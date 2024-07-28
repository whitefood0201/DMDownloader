def reportPrinterDecorater(reportable_func, print_func, report_template: str):
    '''
        Print the `report` with the giving `template`, using the giving `print_func`,
        and return the `result` of the function  
        
        The `reportable_func` should have two return value: `result`, `report`  

        return:
          decorated function
    '''
    def do(*args):
        result, report = reportable_func(*args)
        print_func(report_template % report)
        return result
    return do

printReportPrinterDecorater = lambda reportable_func, report_template: reportPrinterDecorater(reportable_func, print, report_template)
'''
Print the `report` with the giving `template`, using the `print()`
'''

def globalConfigDecorater(configable_func, global_config:dict):
    '''
        Decorat the `global_config` to the function
        The `configable_func` should have two params: `config`, `input`

        return:
          decorated function
    '''
    return lambda input: configable_func(global_config, input)
