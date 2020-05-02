# C++ Notes

## Super C

The most important features that build upon C are:

* function overloading
* `auto` keyword
* reference operator
* namespaces
* implicit `typedef` (for `enum`, `struct` and `union`)

Note: To assign class or function to a namespace use:

```cpp
namespace MyNamespace {
	/* class and function definitions */
}
```

Then, you can use it by invoking `MyNamespace::<class/function>` or with `using namespace MyNamespace` (then it will be available in the whole translation unit / source file).

### Mixing C and C++

To compile C++ code in the C-style the following pattern is used:

```cpp
#ifdef __cplusplus
extern "C" {
#endif

/* definitions and declarations */

#ifdef __cplusplus
}
#endif
```

## C++ standard library

The C++ standard library contains:

* **containers** - data structures holding sequences of objects:
  * *sequence containers* - provide accesses to sequences of elements, like arrays
  * *associative containers* - contain key/value pairs
* **algorithms** - counting, searching, sorting and transforming
* **iterators** - connect containers with algorithms

## Storage duration

There are three types of storage duration:

* **automatic** - automatic object is allocated at the beginning of an enclosing code block
* **static** - declared using the `static` or `extern` keyword (variables declared at global or namespace scope are implicitly `static`):
  * *global static variable*
  * *local static variable* - lifetime from declaration at function scope until program exits
  * *static members* - members of a class not associated with a particular instance of a class
* **thread-local** - each thread will have its own copy of the object that has `thread_local` keyword added to `static` or `extern`

* **dynamic** - allocated and deallocated on request (with `new` and `delete` keywords)

## Values

### `lvalue`

An `lvalue` has both value and address / storage. Examples:

```cpp
int test = 10;
std::string = "hello";
```

Here, everything on left side is an `lvalue`.

Note: Functions are usually `rvalue`, but can be `lvalue` as in case of:

```cpp
int& func() {
	static int var = 0;
	return var;
}

int main() {
	func() = 20;
}
```

Note: Defining argument as a reference is actually defining it as an `lvalue`. For example:

```cpp
void func(int& arg) {
	/* do something with arg */
}
```

In this case, `func(10)` won't work, but the following code will:

```cpp
int x;
func(x);
```

### `rvalue`

An `rvalue` has only value and no address / storage. Examples:

```cpp
int a = 10;
int b = 20;
std::string = "hello";
int c = a + b;
```

Here, everything on right-hand side is an `rvalue` (even `a + b`, as its storage is only temporary, until passed to `c`).

Note: It is possible to hack in order to have a reference to `rvalue`:

```cpp
const int& a = 10;
```

The `const` keyword creates a temporary, invisible variable holding `10`. You can also pass both `lvalue` and `rvalue` as an argument in this manner:

```cpp
void func(const int& arg) {
	/* do something with arg */
}
```

If you want to pass only `rvalue`, do:

```cpp
void func(int&& arg) {
	/* do something with arg */
}
```

Latter function definition is useful as an optimization hack, and is usually paired up with the former definition, as an overloaded function.

## Keywords and identifiers

### `auto`

The `auto` keyword allows compiler to deduce the type of the variable.

### `const`

The `const` keyword can be used to:

* make **function arguments** (pointers and references) read-only
* promise **methods** won't modify current object's state (place `const` keyword after method name and argument list, but before the body brackets)
* disable modification of **member variables** after their initialization

### `mutable`

Permits modification of the class member declared `mutable` even if the containing object is declared `const`.

### `noexcept`

Mark any function with `noexcept` that you are sure cannot throw an exception (syntax same as with `const`). Destructors should be treated as `noexpect`; they should never throw an exception.

Note: You can also use `noexcept(<expression>)` to conditionally mark function as `noexpect` (if and only if `<expression>` evaluates to `true`).

## Exception handling

### Standard exception classes

You can find good information on except class [here](https://en.cppreference.com/w/cpp/header/stdexcept).

### Try-catch

To throw an exception, just use, e.g.:

```cpp
throw std::runtime_error { "Error message" };
```

To catch exception:

```cpp
try {
	/* function that throws exception */
} catch (std::exception &ex) {
	/* handle any exception */
}
```

You can always narrow down handled exceptions, so instead of `std::exception`, you can use, e.g. `std::runtime_error`. Also, you can retrieve the error message by using `what()` method in , for example:

```cpp
try {
	throw std::runtime_error { "Error message" };
} catch (std::runtime_error &ex) {
	cout << "Error: " << ex.what();
}
```

## Patterns

### Initialization

Variables should be initialized with the bracket syntax, as it is the safest (won't generate garbage value):

```cpp
int x {};
float y { 5.0 };
int z[] { 1, 2, 3 };
```

Note: `x` will be initialized to `0`.

### Structured binding declaration

You can do primitive pattern matching, e.g. in error handling by using `return { data, success }` in a function (here: `function()`), and then retrieveng it with `auto [ data, success ] = function();`.

### Future / promise

This is equivalent to conditional variable wait (consumer) and signal (producer), respectively.


