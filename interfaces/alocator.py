from abc import ABC, abstractmethod

class Alocator:

    def __init__(self):
        self._model = []
        self._counter = 1
        self._proposition_mapping = {}
        self._proposition_mapping_inv = {}
        self._optimizers = []

    @staticmethod
    def transform_clauses_to_pseudo_boolean(clause, value=None):
        output = ''
        for literal in clause:
            atom = abs(literal)
            variable = '~x' if literal < 0 else 'x'
            if value is not None:
                output += str(value) + ' ' + variable + str(atom) + " "
            else:
                output += '1 ' + variable + str(atom) + " "
        return output

    @staticmethod
    def transform_clauses_to_pseudo_boolean_inequality(clause, operator, quantity, value=None):
        pseudo_boolean_inequality = Alocator.transform_clauses_to_pseudo_boolean(clause, value)
        pseudo_boolean_inequality += operator + " " + str(quantity) + " ;"
        return pseudo_boolean_inequality

    def _add_to_mapping(self, input):
        if input not in self._proposition_mapping.keys():
            self._proposition_mapping[input] = self._counter
            self._proposition_mapping_inv[self._counter] = input
            self._counter += 1
        return self._proposition_mapping[input]

    def _add_manager_tasks(self, manager, tasks):
        clauses = []
        for task in tasks:
            for day in self._days:
                for period in self._periods:
                    mapping_task_day_period = self._add_to_mapping(task + "_" + day + "_" + period)
                    mapping_manager_task_day_period = self._add_to_mapping(manager + "_" + task + "_" + day + "_" + period)
                    mapping_manager_day_period = self._add_to_mapping(manager + "_" + day + "_" + period)
                    mapping_manager_day = self._add_to_mapping(manager + "_" + day)
                    clauses.append(Alocator.transform_clauses_to_pseudo_boolean_inequality(
                        [-mapping_task_day_period, mapping_manager_task_day_period], '>=', 1))
                    clauses.append(Alocator.transform_clauses_to_pseudo_boolean_inequality(
                        [-mapping_manager_task_day_period, mapping_task_day_period], '>=', 1))
                    clauses.append(Alocator.transform_clauses_to_pseudo_boolean_inequality(
                        [-mapping_manager_task_day_period, mapping_manager_day_period], '>=', 1))
                    clauses.append(Alocator.transform_clauses_to_pseudo_boolean_inequality(
                        [-mapping_manager_day_period, mapping_manager_day], '>=', 1))

        for day in self._days:
            for period in self._periods:
                all_managed_tasks = []
                mapping_manager_day_period = self._add_to_mapping(manager + "_" + day + "_" + period)
                for task in tasks:
                    all_managed_tasks.append(self._add_to_mapping(manager + "_" + task + "_" + day + "_" + period))
                clauses.append(Alocator.transform_clauses_to_pseudo_boolean_inequality(all_managed_tasks, '<=', 1))
                clauses.append(
                    Alocator.transform_clauses_to_pseudo_boolean_inequality([-mapping_manager_day_period] + all_managed_tasks,
                                                                   '>=', 1))

        # manager_day
        for day in self._days:
            all_periods = []
            mapping_manager_day = self._add_to_mapping(manager + "_" + day)
            for period in self._periods:
                all_periods.append(self._add_to_mapping(manager + "_" + day + "_" + period))
            clauses.append(
                Alocator.transform_clauses_to_pseudo_boolean_inequality([-mapping_manager_day] + all_periods, '>=', 1))

        return clauses

    def _add_managers_for_shifted_task(self, managers, task, quantity):
        clauses = []
        all_shifted_task_allocation = []
        for day in self.days:
            for period in self.periods:
                for manager in managers:
                    manager_shifted_task_day_period = self._add_to_mapping(manager + "_" + task + "_" + day + "_" + period)
                    all_shifted_task_allocation.append(manager_shifted_task_day_period)

                    task_day_period = self._add_to_mapping(task + "_" + day + "_" + period)
                    clauses.append(Alocator.transform_clauses_to_pseudo_boolean_inequality(
                        [-manager_shifted_task_day_period, task_day_period], '>=', 1))
        clauses.append(Alocator.transform_clauses_to_pseudo_boolean_inequality(all_shifted_task_allocation, '=', quantity))
        return clauses

    def _restriction_exclusive_managers_tasks_for_day_period(self, managers, tasks):
        clauses = []
        for day in self._days:
            for period in self._periods:
                for task in tasks:
                    all_tasks = []
                    for manager in managers:
                        manager_task_day_period = self._add_to_mapping(manager + "_" + task + "_" + day + "_" + period)
                        all_tasks.append(manager_task_day_period)
                    clauses.append(Alocator.transform_clauses_to_pseudo_boolean_inequality(all_tasks, '<=', 1))
                for manager in managers:
                    all_tasks = []
                    for task in tasks:
                        manager_task_day_period = self._add_to_mapping(manager + "_" + task + "_" + day + "_" + period)
                        all_tasks.append(manager_task_day_period)
                    clauses.append(Alocator.transform_clauses_to_pseudo_boolean_inequality(all_tasks, '<=', 1))
        return clauses

    def _add_task_days_periods_quantity(self, task, max_quantity):
        clauses = []
        for day in self._days:
            for period in self._periods:
                clauses.append(self._add_to_mapping(task + "_" + day + "_" + period))
        return [Alocator.transform_clauses_to_pseudo_boolean_inequality(clauses, '=', max_quantity)]

    def _set_paired_tasks(self, task_1, task_2):
        clauses = []
        for day in self._days:
            for period in self._periods:
                task1_day_period = self._add_to_mapping(task_1 + "_" + day + "_" + period)
                task2_day_period = self._add_to_mapping(task_2 + "_" + day + "_" + period)
                clauses.append(
                    Alocator.transform_clauses_to_pseudo_boolean_inequality([-task1_day_period, task2_day_period], '>=', 1))
                clauses.append(
                    Alocator.transform_clauses_to_pseudo_boolean_inequality([task1_day_period, -task2_day_period], '>=', 1))
        return clauses

    def _set_consecutive_tasks(self, task_1, tasks_2):
        clauses = []
        for day in self._days:
            clause = []
            task1_day_period = self._add_to_mapping(task_1 + "_" + day + "_" + self.periods[0])
            for task_2 in tasks_2:
                clause.append(self._add_to_mapping(task_2 + "_" + day + "_" + self.periods[1]))
            clauses.append(Alocator.transform_clauses_to_pseudo_boolean_inequality([-task1_day_period] + clause, '>=', 1))

            task1_day_period = self._add_to_mapping(task_1 + "_" + day + "_" + self.periods[1])
            clause = []
            for task_2 in tasks_2:
                clause.append(self._add_to_mapping(task_2 + "_" + day + "_" + self.periods[0]))
            clauses.append(Alocator.transform_clauses_to_pseudo_boolean_inequality([-task1_day_period] + clause, '>=', 1))

            clause = []
            task1_day_period = self._add_to_mapping(task_1 + "_" + day + "_" + self.periods[2])
            for task_2 in tasks_2:
                clause.append(self._add_to_mapping(task_2 + "_" + day + "_" + self.periods[3]))
            clauses.append(Alocator.transform_clauses_to_pseudo_boolean_inequality([-task1_day_period] + clause, '>=', 1))

            task1_day_period = self._add_to_mapping(task_1 + "_" + day + "_" + self.periods[3])
            clause = []
            for task_2 in tasks_2:
                clause.append(self._add_to_mapping(task_2 + "_" + day + "_" + self.periods[2]))
            clauses.append(Alocator.transform_clauses_to_pseudo_boolean_inequality([-task1_day_period] + clause, '>=', 1))

        return clauses

    def _task_twice_a_week_has_paired_days_periods(self, task):
        clauses = []
        for period in self._periods:
            task_seg_period = self._add_to_mapping(task + "_" + "seg" + "_" + period)
            task_qua_period = self._add_to_mapping(task + "_" + "qua" + "_" + period)
            task_sex_period = self._add_to_mapping(task + "_" + "sex" + "_" + period)
            clauses.append(Alocator.transform_clauses_to_pseudo_boolean_inequality([-task_seg_period, task_qua_period], '>=', 1))
            clauses.append(Alocator.transform_clauses_to_pseudo_boolean_inequality([-task_sex_period, task_qua_period], '>=', 1))
            clauses.append(
                Alocator.transform_clauses_to_pseudo_boolean_inequality([-task_qua_period, task_seg_period, task_sex_period],
                                                               '>=', 1))

            task_ter_period = self._add_to_mapping(task + "_" + "ter" + "_" + period)
            task_qui_period = self._add_to_mapping(task + "_" + "qui" + "_" + period)
            clauses.append(Alocator.transform_clauses_to_pseudo_boolean_inequality([-task_ter_period, task_qui_period], '>=', 1))
            clauses.append(Alocator.ransform_clauses_to_pseudo_boolean_inequality([-task_qui_period, task_ter_period], '>=', 1))
        return clauses

    def _manager_maximum_a_day(self, manager, maximum):
        clauses = []
        for day in self._days:
            clause = []
            for period in self._periods:
                manager_day_period = self._add_to_mapping(manager + "_" + day + "_" + period)
                clause.append(manager_day_period)
            clauses.append(Alocator.transform_clauses_to_pseudo_boolean_inequality(clause, '<=', maximum))
        return clauses

    def _create_optimizer(self, manager_opt, manager, _days, _periods):
        manager_opt_mapping = self._add_to_mapping(manager_opt)
        clauses = []
        for day in _days:
            for period in _periods:
                manage_day_period = self._add_to_mapping(manager + "_" + day + "_" + period)
                clauses.append(
                    Alocator.transform_clauses_to_pseudo_boolean_inequality([-manager_opt_mapping, manage_day_period], '>=', 1))
        return clauses

    def _create_max_function_with_optimizer(self, optimizers, value):
        clause = []
        for optimizer in optimizers:
            optimizer_mapping = self._add_to_mapping(optimizer)
            clause.append(optimizer_mapping)
        return Alocator.transform_clauses_to_pseudo_boolean(clause, -value)

    @abstractmethod
    def alocar_horarios(self):
        pass
