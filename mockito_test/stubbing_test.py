from test_base import *
from mockito import mock, when, verify, times, any, StubbingError

class StubbingTest(TestBase):
  def testStubsWithReturnValue(self):
    theMock = mock()
    when(theMock).getStuff().thenReturn("foo")
    when(theMock).getMoreStuff(1, 2).thenReturn(10)
    
    self.assertEquals("foo", theMock.getStuff())
    self.assertEquals(10, theMock.getMoreStuff(1, 2))
    self.assertEquals(None, theMock.getMoreStuff(1, 3))
    
  def testStubsWhenNoArgsGiven(self):
      theMock = mock()
      when(theMock).getStuff().thenReturn("foo")
      when(theMock).getWidget().thenReturn("bar")
  
      self.assertEquals("foo", theMock.getStuff())
      self.assertEquals("bar", theMock.getWidget())     
    
  def testStubsConsecutivelyWhenNoArgsGiven(self):
      theMock = mock()
      when(theMock).getStuff().thenReturn("foo").thenReturn("bar")
      when(theMock).getWidget().thenReturn("baz").thenReturn("baz2")
  
      self.assertEquals("foo", theMock.getStuff())
      self.assertEquals("bar", theMock.getStuff())
      self.assertEquals("bar", theMock.getStuff())        
      self.assertEquals("baz", theMock.getWidget())
      self.assertEquals("baz2", theMock.getWidget())
      self.assertEquals("baz2", theMock.getWidget())
    
  def testStubsWithException(self):
    theMock = mock()
    when(theMock).someMethod().thenRaise(Exception("foo"))
    
    self.assertRaisesMessage("foo", theMock.someMethod)

  def testStubsAndVerifies(self):
    theMock = mock()
    when(theMock).foo().thenReturn("foo")
    
    self.assertEquals("foo", theMock.foo())
    verify(theMock).foo()

  def testStubsVerifiesAndStubsAgain(self):
    theMock = mock()
    
    when(theMock).foo().thenReturn("foo")
    self.assertEquals("foo", theMock.foo())
    verify(theMock).foo()
    
    when(theMock).foo().thenReturn("next foo")    
    self.assertEquals("next foo", theMock.foo())
    verify(theMock, times(2)).foo()
    
  def testOverridesStubbing(self):
    theMock = mock()
    
    when(theMock).foo().thenReturn("foo")
    when(theMock).foo().thenReturn("bar")
    
    self.assertEquals("bar", theMock.foo())

  def testStubsAndInvokesTwiceAndVerifies(self):
    theMock = mock()
    
    when(theMock).foo().thenReturn("foo")
    
    self.assertEquals("foo", theMock.foo())
    self.assertEquals("foo", theMock.foo())

    verify(theMock, times(2)).foo()

  def testStubsAndReturnValuesForMethodWithSameNameAndDifferentArguments(self):
    theMock = mock()
    when(theMock).getStuff(1).thenReturn("foo")
    when(theMock).getStuff(1, 2).thenReturn("bar")
    
    self.assertEquals("foo", theMock.getStuff(1))
    self.assertEquals("bar", theMock.getStuff(1, 2))
    
  def testStubsAndReturnValuesForMethodWithSameNameAndDifferentNamedArguments(self):
    repo = mock()
    when(repo).findby(id=6).thenReturn("John May")
    when(repo).findby(name="John").thenReturn(["John May", "John Smith"])
    
    self.assertEquals("John May", repo.findby(id=6))
    self.assertEquals(["John May", "John Smith"], repo.findby(name="John"))
    
  def testStubsForMethodWithSameNameAndNamedArgumentsInArbitraryOrder(self):
    theMock = mock()
    
    when(theMock).foo(first=1, second=2, third=3).thenReturn(True)
    
    self.assertEquals(True, theMock.foo(third=3, first=1, second=2))
    
  def testStubsMethodWithSameNameAndMixedArguments(self):
    repo = mock()
    when(repo).findby(1).thenReturn("John May")
    when(repo).findby(1, active_only=True).thenReturn(None)
    when(repo).findby(name="Sarah").thenReturn(["Sarah Connor"])
    when(repo).findby(name="Sarah", active_only=True).thenReturn([])
    
    self.assertEquals("John May", repo.findby(1))
    self.assertEquals(None, repo.findby(1, active_only=True))
    self.assertEquals(["Sarah Connor"], repo.findby(name="Sarah"))
    self.assertEquals([], repo.findby(name="Sarah", active_only=True))
    
  def testStubsWithChainedReturnValues(self):
    theMock = mock()
    when(theMock).getStuff().thenReturn("foo").thenReturn("bar").thenReturn("foobar")
    
    self.assertEquals("foo", theMock.getStuff())
    self.assertEquals("bar", theMock.getStuff())
    self.assertEquals("foobar", theMock.getStuff())

  def testStubsWithChainedReturnValuesAndException(self):
    theMock = mock()
    when(theMock).getStuff().thenReturn("foo").thenReturn("bar").thenRaise(Exception("foobar"))
    
    self.assertEquals("foo", theMock.getStuff())
    self.assertEquals("bar", theMock.getStuff())
    self.assertRaisesMessage("foobar", theMock.getStuff)

  def testStubsWithChainedExceptionAndReturnValue(self):
    theMock = mock()
    when(theMock).getStuff().thenRaise(Exception("foo")).thenReturn("bar")
    
    self.assertRaisesMessage("foo", theMock.getStuff)
    self.assertEquals("bar", theMock.getStuff())

  def testStubsWithChainedExceptions(self):
    theMock = mock()
    when(theMock).getStuff().thenRaise(Exception("foo")).thenRaise(Exception("bar"))
    
    self.assertRaisesMessage("foo", theMock.getStuff)
    self.assertRaisesMessage("bar", theMock.getStuff)

  def testStubsWithReturnValueBeingException(self):
    theMock = mock()
    exception = Exception("foo")
    when(theMock).getStuff().thenReturn(exception)
    
    self.assertEquals(exception, theMock.getStuff())
    
  def testLastStubbingWins(self):
    theMock = mock()
    when(theMock).foo().thenReturn(1)
    when(theMock).foo().thenReturn(2)
    
    self.assertEquals(2, theMock.foo())
    
  def testStubbingOverrides(self):
    theMock = mock()
    when(theMock).foo().thenReturn(1)
    when(theMock).foo().thenReturn(2).thenReturn(3)
    
    self.assertEquals(2, theMock.foo())    
    self.assertEquals(3, theMock.foo())    
    self.assertEquals(3, theMock.foo())   
    
  def testStubsWithMatchers(self):
    theMock = mock()
    when(theMock).foo(any()).thenReturn(1)
    
    self.assertEquals(1, theMock.foo(1))    
    self.assertEquals(1, theMock.foo(100))   
    
  def testStubbingOverrides2(self):
    theMock = mock()
    when(theMock).foo(any()).thenReturn(1)
    when(theMock).foo("oh").thenReturn(2)
    
    self.assertEquals(2, theMock.foo("oh"))    
    self.assertEquals(1, theMock.foo("xxx"))   
    
  def testDoesNotVerifyStubbedCalls(self):
    theMock = mock()
    when(theMock).foo().thenReturn(1)

    verify(theMock, times=0).foo()

  def testStubsWithMultipleReturnValues(self):
    theMock = mock()
    when(theMock).getStuff().thenReturn("foo", "bar", "foobar")
    
    self.assertEquals("foo", theMock.getStuff())
    self.assertEquals("bar", theMock.getStuff())
    self.assertEquals("foobar", theMock.getStuff())

  def testStubsWithChainedMultipleReturnValues(self):
    theMock = mock()
    when(theMock).getStuff().thenReturn("foo", "bar").thenReturn("foobar")
    
    self.assertEquals("foo", theMock.getStuff())
    self.assertEquals("bar", theMock.getStuff())
    self.assertEquals("foobar", theMock.getStuff())

  def testStubsWithMultipleExceptions(self):
    theMock = mock()
    when(theMock).getStuff().thenRaise(Exception("foo"), Exception("bar"))
    
    self.assertRaisesMessage("foo", theMock.getStuff)
    self.assertRaisesMessage("bar", theMock.getStuff)

  def testStubsWithMultipleChainedExceptions(self):
    theMock = mock()
    when(theMock).getStuff().thenRaise(Exception("foo"), Exception("bar")).thenRaise(Exception("foobar"))
    
    self.assertRaisesMessage("foo", theMock.getStuff)
    self.assertRaisesMessage("bar", theMock.getStuff)
    self.assertRaisesMessage("foobar", theMock.getStuff)
    
  def testLeavesOriginalMethodUntouchedWhenCreatingStubFromRealClass(self):
    class Person:
      def get_name(self):
        return "original name"

    # given
    person = Person()
    mockPerson = mock(Person)

    # when
    when(mockPerson).get_name().thenReturn("stubbed name")

    # then
    self.assertEquals("stubbed name", mockPerson.get_name())
    self.assertEquals("original name", person.get_name(), 'Original method should not be replaced.')

  def testStubVerifiedOnClass(self):
    class Person:
      def get_name(self, a, d=None):
        pass

    m = mock(Person)
    when(m).get_name('a').thenReturn("stubbed name")
    try:
      when(m).get_name().thenReturn("stubbed name")
    except StubbingError:
      pass
    else:
      self.assertTrue(False, "StubbingError not raised")

  def testStubVerifiedOnInstance(self):
    class Person:
      def get_name(self, a, d=None):
        return "XXX"
      @staticmethod
      def bar_name(a):
        return a

    person = Person()
    m = mock(person)
    when(m).get_name('a').thenReturn("stubbed name")
    when(m).bar_name('a').thenReturn("stubbed name")
    try:
      when(m).get_name().thenReturn("stubbed name")
    except StubbingError:
      pass
    else:
      self.assertTrue(False, "StubbingError not raised")
    try:
      when(m).bar_name().thenReturn("stubbed name")
    except StubbingError:
      pass
    else:
      self.assertTrue(False, "StubbingError not raised")

  def testChainableStubs(self):
    person = mock(chainable=True)
    person.needs().help(10)
    verify(person).needs().help(10)

    that = mock(chainable=True)
    when(that).a().b(10).thenReturn(20)
    x = that.a().b(10)
    self.assertEquals(x, 20)


# TODO: verify after stubbing and vice versa

if __name__ == '__main__':
  unittest.main()
