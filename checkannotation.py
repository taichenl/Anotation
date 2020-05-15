from goody import type_as_str
import inspect

class Check_All_OK:
    """
    Check_All_OK class implements __check_annotation__ by checking whether each
      annotation passed to its constructor is OK; the first one that
      fails (by raising AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """
       
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_All_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        for annot in self._annotations:
            check(param, annot, value, check_history+'Check_All_OK check: '+str(annot)+' while trying: '+str(self)+'\n')


class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (by raising AssertionError) this classes raises AssertionError and prints
      its failure, along with a list of all annotations tried followed by the
      check_history.
    """
    
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_Any_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        failed = 0
        for annot in self._annotations: 
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param)+' failed annotation check(Check_Any_OK): value = '+repr(value)+\
                         '\n  tried '+str(self)+'\n'+check_history                 
def tree_list(atree):
    if atree == None:
        return None
    else:
        return [atree.value, tree_list(atree.left), tree_list(atree.right)]

def Trace_Calls:
    def __init__(self, f):
        self._f = f
        self._calls = 0
    
    def __call__(self, arg):
        self.calls += 1
        return self._f(arg)
    
    def called(self):
        return self._calls

    def reset(self):
        self.calls = 0
        
class Check_Annotation:
    # To begin, by binding the class attribute to True means checking can occur
    #   (but only when self._checking_on is bound to True too)
    checking_on  = True
  
    # For checking the decorated function, bind self._checking_on as True too
    def __init__(self, f):
        self._f = f
        self._checking_on = True
        
    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.  
    def check(self,param,annot,value,check_history=''):
        
        # Define local functions for checking, list/tuple, dict, set/frozenset,
        #   lambda/functions, and str (str for extra credit)
        # Many of these local functions called by check, call check on their
        #   elements (thus are indirectly recursive)

        # To begin, get check's function annotation and compare it to its arguments
        if annot == None:
            pass
        elif type(annot) is type:
            assert isinstance(value, annot), str(param) + ' failed annotation check(wrong2) : value = ' + str(value) +'\n was type ' + str(type(value)) + '...should be type ' + str(type(annot))
        elif isinstance(annot, list):
            assert isinstance(value, list), str(param) + ' failed annotation check(wrong) : value = ' + str(value) +'\n was type ' + str(type(value)) + '...should be type ' + str(type(annot)) + '\n' + check_history
            if len(annot) == 1:
                for i in value:
                    self.check(param, annot[0], i, check_history + 'List[' + str(i) + '] check:' + str(type(i)))
            else:
                assert len(annot) == len(value), str(param) + 'failed annotation check (wrong number of elements): value = ' + str(value) + '\n annotaion had ' + str(len(annot)) + 'element' + str(annot) + '\n' + check_history
                for i in range(0, len(annot)):
                    self.check(param, annot[i], value[i], check_history + 'List[' + str(i) + '] check:' + str(i))  
        elif isinstance(annot, tuple):
            assert isinstance(value, tuple), str(param) + ' failed annotation check(wrong) : value = ' + str(value) +'\n was type ' + str(type(value)) + '...should be type ' + str(type(annot)) + '\n' + check_history
            if len(annot) == 1:
                for i in value:
                    self.check(param, annot[0], i, check_history + 'List[' + str(i) + '] check:' + str(type(i)))
            else:
                assert len(annot) == len(value), str(param) + 'failed annotation check (wrong number of elements): value = ' + str(value) + '\n annotaion had ' + str(len(annot)) + 'element' + str(annot) + '\n' + check_history
                for i in range(0, len(annot)):
                    self.check(param, annot[i], value[i], check_history + 'List[' + str(i) + '] check:' + str(i))  
        elif isinstance(annot, dict):
            assert isinstance(value, dict), 'mmmm'
            assert len(annot) == 1, '...'
            for i in annot.keys():
                v = annot[i]
            for a, b in value.items():
                self.check(param, i,a, check_history + ' ')
                self.check(param, v,b, check_history + ' ') 
        elif isinstance(annot, set):
            assert isinstance(value, set), '...'
            assert len(annot) == 1, 'ssss'
            i = annot.pop()   
            for a in value:
                self.check(param, i, a, check_history + ' ')
        elif isinstance(annot, frozenset):
            assert isinstance(value, frozenset), '...'
            assert len(annot) == 1, 'ssss'
            list1 = [x for x in annot]
            for a in value:
                self.check(param, list1[0], a, check_history + ' ')
        elif inspect.isfunction(annot):
            assert len(annot.__code__.co_varnames) == 1, 'ssss'
            try:
                result = annot(value)
                assert result, 'xxx'
            except Exception:
                assert False, 'bbb'
        elif isinstance(annot, str):
            pass
            """try:
                a = eval(annot, self.dict)
                assert a
            except Exception:
                assert False, 'vvv'"""
        else:
            try:
                annot.__check_annotation__(self.check, param, value, check_history)
            except AttributeError:
                assert False, '   '
            except Exception as Ex:
                if Ex is AssertionError:
                    pass
                else:
                    assert False, '   '
    
                
        
        
    # Return result of calling decorated function call, checking present
    #   parameter/return annotations if required
    def __call__(self, *args, **kargs):
        
        # Return an ordereddict of the parameter/argument bindings: it's a special
        #   kind of dict, binding the function header's parameters in order
        def param_arg_bindings():
            f_signature  = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args,**kargs)
            for param in f_signature.parameters.values():
                if not (param.name in bound_f_signature.arguments):
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments

        # If annotation checking is turned off at the class or function level
        #   just return the result of calling the decorated function
        # Otherwise do all the annotation checking
        if not self.checking_on:
            return self._f
        
        self.dict = param_arg_bindings()
        
        annotations = self._f.__annotations__
        try:
            # Check the annotation for each of the parameters that is annotated
            for i in self.dict.keys():
                if i in annotations.keys():
                    self.check(i, annotations[i], self.dict[i])

            # Compute/remember the value of the decorated function
            result = self._f(*args, **kargs)
            # If 'return' is in the annotation, check it
            if 'return' in annotations.keys():
                self.dict['_return'] = result
                self.check('return', annotations['return'], self.dict['_return'])
            # Return the decorated answer
            return result
            #remove after adding real code in try/except
            
        # On first AssertionError, print the source lines of the function and reraise 
        except AssertionError:
            
            #print(80*'-')
            #for l in inspect.getsourcelines(self._f)[0]: # ignore starting line #
            #    print(l.rstrip())
            #print(80*'-')
            raise



  
if __name__ == '__main__':  
       
    # an example of testing a simple annotation  
    #driver tests
    import driver
    driver.default_file_name = 'bscp4F19.txt'
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
