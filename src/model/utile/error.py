class WorkNotFoundError(Exception):
    def __init__(self, work_name: str):
        self.message = "Work[{0}] not found in workflow.".format(work_name)
        super().__init__(self.message)

class AttributeNotFoundError(Exception):
    '''The attribute not found in work'''
    def __init__(self, attribute: str):
        self.message = "The attribute[{0}] not found in work.".format(attribute)
        super().__init__(self.message)

class NoActionTypeError(Exception):
    def __init__(self, action_type: str):
        self.message = "No action named ActionType[{0}].".format(action_type)
        super().__init__(self.message)

class NoCheckerError(Exception):
    def __init__(self, checker_type: str):
        self.message = "No checker named StructureChecker[{0}].".format(checker_type)
        super().__init__(self.message)