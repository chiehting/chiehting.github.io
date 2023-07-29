---
date: 2017-12-21 00:00:00 +0800
updated: 2023-07-14T11:25:49+08:00
title: Relearn PHP
category: php
tags: [php, programmingLanguage]
type: note
author: Chiehting
status: 🌲
sourceType: 📜️
sourceURL: https://www.php.net/manual/en/
---

PHP7 release也一段時間了,最近在開發常會看到相關的文章,最近抽個空好好來重新學習PHP.

<!--more-->

## Preface

"PHP: Hypertext Preprocessor",官方網站表明PHP很適合做web development,但是並不局限於此,亦可做Process Control,但是依據個人經驗,PHP5.3以下的版本做浮點數的運算不是很精準.

另外在2015年PHP7問世,效率更是翻倍,但是有著相容性問題,系統升級前需要做好測試.

## 環境建置

採用[Virtualbox][]+[Vagrant][]來架設環境,執行步驟如下:

1. 安裝Virtualbox與Vagrant,這邊就不講解了,幾本上下一步到底
2. 下載Vagrant box

    ```bash
    $ vagrant box add rasmus/php7dev
    $ vagrant init rasmus/php7dev
    # 確認box list
    $ vagrant box list
    ```

3. git clone

    ```bash
    git clone https://github.com/rlerdorf/php7dev.git
    cd php7dev
    ```

4. 共享目錄設定,編輯php7dev.yaml檔案

    ```yaml
    folders:
    - map: www
      to: /var/www/default
    ```

5. 啟動VM、進入VM、暫停VM、註銷VM

    ```bash
    # 啟動VM
    $ vagrnat up
    # 進入VM
    $ vagrant ssh
    # 暫停VM
    $ vagrant halt
    # 註銷VM
    $ vagrant destroy --force
    ```

6. 建立檔案

    ```bash
    # 建立一個 index.php 檔案, 運行可以顯示 PHP 資訊
    $ echo "<?php echo phpinfo(); ?>" > /var/www/default/index.php
    ```

環境建立完成,再來可以透過Browser輸入`http://192.168.7.7/`來進入站台.

---

## Type

PHP是屬於弱型別的語言,也就是變數不用宣告就直接可以做assign,但是資料型態還是程式語言的重點基礎之一,還是要好好的認識一下.

* Boolean:通常是一個常量`true`或`false`,不區分大小寫.

    ```php
    $var1 = true;
    $var2 = False;
    ```

* Integer:是一個*有限整數*((2^32)-1),集合中的某個數Z = {..., -2, -1, 0, 1, 2, ...}

    ```php
    //自PHP5.4.0後可以採用十進制、十六進制、八進制、二進制
    $var = 1234; //十進制
    $var = -123; //負數
    $var = 0123; //八進制
    $var = 0x1A; //十六進制
    $var = 0b11111111; //二進制
    ```

* Float:也就是小數,長度取決於平台. 另外不要相信浮點數結果精確到了最後一位,也永遠不要比較兩個浮點數是否相等,如果確實需要更高的精度,應該使用*任意精度數學函數*或者*gmp函數*.

    ```php
    $var = 1.23456789;
    ```

* String:每個字都是由一系列的character(字元)組成(字的編碼),每個字元相當於一個byte(2^8),也就是說PHP只支援到256-character,因此不支援Unicode(因為過長).

    ```php
    $name = 'ting';
    $var = 'my name is $name'; //全視為為字串
    $var = "my name is $name"; //對$name進行解析
    //Heredoc結構,自PHP5.3起,會對變數進行解析
    $var = <<<EOT
    my name is $name
        EOT;
    //newcode結構,全視為字串,不對變數進行解析
    $var = <<<'EOT'
    my name is $name
        EOT;
    ```

* Array:是一組有序映射,官網說"it can be treated as an array, list (vector), hash table (an implementation of a map), dictionary, collection, stack, queue, and probably more.",由此可見他的功能很廣.

    ```php
    $array = array(
        "foo" => "bar",
    );
    // 自 PHP 5.4 起
    $array = [
        "foo" => "bar",
    ];
    ```

* Object:物件.

    ```php
    class foo
    {
        function do_foo()
        {
            echo "Doing foo.";
        }
    }
    $bar = new foo;
    $bar->do_foo();
    ```

* Resource:資源,通常可能是連接資料庫、開啟文件.
* NULL:指一個變數還未被assign,或著被釋放

    ```php
    $var = NULL;
    ```

* Callback

    ```php
    error_reporting(E_ALL);
    function increment(&$var)
    {
        $var++;
    }
    $a = 0;
    call_user_func('increment', $a);
    echo $a."\n";
    call_user_func_array('increment', array(&$a));
    echo $a."\n";
    ```

---

## Variables

變數的命名很重要,程式要寫的漂亮的重點之一就是變數的命名.

1. 基本變數:PHP中宣告變數是使用符號*$*後面再跟上'^\[a-zA-Z][\_]?\[\x7f-\xff]\[a-zA-Z0-9_\x7f-\xff]\*',且命名是有大小寫的區別.

    ```php
    $var = 'Bob';
    $bar = &$var; //$bar被assign變數$var,且記憶體位置相同
    ```

2. 全域變數與區域變數

    ```php
    $a = 1;
    function Test()
    {
        global $a;
        $b = 2;
        echo ($a+$b);
    }
    echo $b; //Undefined variable
    Test();
    ```

3. Static variable:靜態變數只會在函數中出現,當程序離開函式,其值不丟失.從下面範例可以發現,在$b被宣告時,都還是NULL的狀態,宣告後才會取回值.

    ```php
    function Test()
    {
        var_dump($b);
        static  $b = 0;
        var_dump($b);
        echo (++$b);
    }
    Test();
    ```

4. Variable variables:變數的名稱也是變數,這樣的特性讓程式變得更彈性.

    ```php
    $a = 'hello';
    $hello = 'world';
    $world = 'a';
    echo $a.'<br/>';
    echo $$a.'<br/>';
    echo $$$a.'<br/>';
    echo "$a ${$a} <br/>";
    echo "$a $hello <br/>";
    ```

---

## Constants

常量定義好後,就無法變更,且長量名稱區分大小寫.

```php
define("version","0.1");
//magic constants
function a(){
    echo __function__;
}
function b(){
    echo __function__;
}
echo a();
echo b();
```

---

## Operators

運算子有先後順序,個人習慣將運算子拆開,一來確保程式的穩定度,二來增加程式的可讀性

```php
$a = true ? 0 : true ? 1 : 2; // (true ? 0 : true) ? 1 : 2 = 2
$a = 1;
$b = 2;
$a = $b += 3; // $a = ($b += 3) -> $a = 5, $b = 5
```

1. 算數運算子

    ```php
    echo (5 + 3)."\n"; //prints 8
    echo (5 - 3)."\n"; //prints 2
    echo (5 * 3)."\n"; //prints 15
    echo (15 / 3)."\n"; //prints 5
    echo (5 % 3)."\n"; //prints 2
    echo (5  3)."\n"; //prints 125
    ```

2. 位元運算子

    ```php
    echo 0b0010 & 0b0010; //print 2
    echo 0b0010 | 0b0010; //print 2
    echo 0b0010 ^ 0b0011; //print 1
    echo ~0b0101; //print -6
    echo 0b0010 >> 1; //print 1
    echo 0b0010 << 1; //print 4
    ```

3. 比較運算子

    ```php
    var_dump(0 == "a"); //0 == 0 -> true
    var_dump("1" == "01"); //1 == 1 -> true
    var_dump("10" == "1e1"); //10 == 10 -> true
    var_dump(100 == "1e2"); //100 == 100 -> true
    var_dump("1e1"); //string '1e1'
    ```

4. 錯誤控制運算子

    ```php
    @include('./not_exist_file.php');
    $x = @$a["name"];
    ```

5. Execution Operators:以前都用exec(),這個好方便

    ```php
    $mkdir = `mkdir new floder`;
    $output = `ls -al`;
    echo "<pre>$output</pre>";
    ```

6. 遞增/遞減運算子

    ```php
    $a = 5;
    echo $a++."<br />"; //print 5
    echo ++$a."<br />"; //print 7
    echo $a--."<br />"; //print 7
    echo --$a."<br />"; //print 5
    ```

7. Logical Operators

    ```php
    //"||" 比 "or" 的優先级高,"&&" 比 "and" 的優先级高
    $e = false || true; //bool(true),等同于：($e = (false || true))
    $f = false or true; //bool(false),等同于：(($f = false) or true)
    $g = true && false; //bool(false),等同于：($g = (true && false))
    $h = true and false; //bool(true),等同于：(($h = true) and false)
    ```

8. String Operators

    ```php
    $a = "Hello ";
    $b = $a . "World!"; // now $b contains "Hello World!"
    $a = "Hello ";
    $a .= "World!";     // now $a contains "Hello World!"
    ```

9. Array Operators

    ```php
    $a = array("a" => "apple", "b" => "banana");
    $b = array("a" => "pear", "b" => "strawberry", "c" => "cherry");
    $c = $a + $b; // Union of $a and $b
    var_dump($c); // print array(3) {["a"]=>"apple",["b"]=>"banana",["c"]=>"cherry"}
    ```

10. Type Operators

    ```php
    class ParentClass{}
    class MyClass extends ParentClass{}
    $a = new MyClass;
    var_dump($a instanceof MyClass); //bool(true)
    var_dump($a instanceof ParentClass); //bool(true)
    ```

---

## Control Structures

通常要呈現一個商業邏輯都會透過流程控制來表示,而每種商業邏輯呈現的方法百百種,所以要築構一支好的程式,對流程控制的熟悉度不可少.

1. if else

    ```php
    if ($a > $b):
        echo "a is bigger than b";
    elseif ($a < $b):
        echo "a is smaller than b";
    else:
        echo "a is equal b";
    endif
    ```

2. while:循環語法之一,在遞迴中很好用

    ```php
    while ($i <= 10):
        echo $i++;
    endwhile
    ```

3. do-while:跟while很像,差異在於while在執行前做判斷,do-while在執行後做判斷.

    ```php
    do {
       echo $i;
    } while ($i <= 10);
    ```

4. for

    ```php
    for (;;):
        if ($i > 10):
            break;
        endif;
        echo $i;
        $i++;
    endfor;
    ```

5. foreach:用來解構array很好用

    ```php
    foreach (array(1, 2, 3, 4) as $value):
        $value = $value * 2;
    endforeach;
    ```

6. break

    ```php
    $arr = array('one', 'two', 'three', 'four', 'stop', 'five');
    while (list (, $val) = each($arr)) {
        if ($val == 'stop') {
            break;    /* You could also write 'break 1;' here. */
        }
        echo "$val<br />\n";
    }
    ```

7. continue

    ```php
    for ($i = 0; $i < 5; ++$i) {
        if ($i == 2)
            continue;
        print "$i\n";
    }
    ```

8. switch:在做Boolean值判斷的時候建議使用if else,若做值得判斷則可使用switch

    ```php
    switch ($i) {
        case 0:
            echo "i equals 0";
            break;
        case 1:
        case 2:
            echo "i equals to 1, 2";
            break;
        default:
            echo "i is not equal to 0, 1 or 2";
    }
    ```

9. declare:Zend引擎每執行1條低級語句就去執行一次register\_tick\_function()注冊的函數

    ```php
    declare(ticks=1);
    // A function called on each tick event
    function tick_handler() {
        echo "tick_handler() called\n";
    }
    register_tick_function('tick_handler');
    $a = 1;
    if ($a > 0) {
        $a += 2;
        print($a);
    }
    ```

10. return:如果在全局範圍中調用,則當前腳本文件中止運行.
11. require/include/require\_once/include\_once

    ```php
    require('somefile.php'); //若找不到檔案發出E_COMPILE_ERROR级别錯誤,並終止程序
    include('somefile.php'); //若找不到檔案發出E_WARNING级别錯誤,繼續程序
    require_once('somefile.php'); //和require一樣,但已經包含過的檔案則不會再包含
    include_once('somefile.php'); //和include一樣,但已經包含過的檔案則不會再包含
    ```

12. goto:只在PHP 5.3以上版本有效,跳轉至改文件的目標.目標位置只能位於同一個文件和作用域,也就是說無法跳出一個函數或類方法,也無法跳入到另一個函數.也無法跳入到任何循環或者switch結構中.可以跳出循環或者switch,通常的用法是用goto代替多層的break.

    ```php
    //下面結果輸出Bar
    goto a;
    echo 'Foo';
    a:
    echo 'Bar';
    ```

---

### Function

這邊要注意部分預設函式是跟著extension加載的,例如mysql\_connect()、imagecreatetruecolor()等,所以必須知道自己的環境是否有這些extension,可以用phpinfo()或get\_loaded\_extensions()來查詢.
函數名稱的命名很重要,好的命名可以讓程式可讀性提升,更好維護.

1. User-defined functions

    ```php
    function sum($a, $b): float {
        return $a + $b;
    }
    ```

2. Variable functions

    ```php
    function foo() {
        echo "In foo()<br />\n";
    }
    $func = 'foo';
    $func(); //This calls foo()
    ```

3. Anonymous functions

    ```php
    echo preg_replace_callback('~-([a-z])~', function ($match) {
        return strtoupper($match[1]);
    }, 'hello-world');
    ```

---

### Classes and Objects

自從PHP5後的版本有著較好的效能與功能

1. class:每個類別都有自己的constants、variables與function,並且可使用$this來調用自己.

    ```php
    class SimpleClass
    {
        // property declaration
        public $var = 'a default value';
        // method declaration
        public function displayVar() {
            echo $this->var;
        }
    }
    ```

2. Object Assignment:宣告物件的兩種方式.

    ```php
    Class Object{
       public $foo="bar";
    };
    $objectVar = new Object();
    $reference =& $objectVar;
    $assignment = $objectVar;
    $objectVar=null;
    var_dump($objectVar); //NULL
    var_dump($reference); //NULL,指向同樣的記憶體,所以$objectVar=null被註銷時,一併註銷
    var_dump($assignment); //object(Object),被clone
    ```

3. extends:一個class可以申明繼承另一個class的方法與屬性,不支援多個繼承.可以使用同名稱覆蓋父類別的方法,但是父類別使用final,則不能被覆蓋.被覆蓋的方法或屬性,可以透過parent::來訪問.

    ```php
    class ExtendClass extends SimpleClass
    {
        // Redefine the parent method
        function displayVar()
        {
            echo "Extending class\n";
            parent::displayVar();
        }
    }
    ```

4. Properties,類別的成員.

    ```php
    class SimpleClass
    {
       public $var1 = (1+2);
       public $var2 = myConstant;
       public $var3 = array(true, false);
   }
    ```

5. Class Constants:在類別中不變的值.

    ```php
    class MyClass
    {
        const constant = 'constant value';
        function showConstant() {
            echo  self::constant . "\n";
        }
    }
    ```

6. Autoloading Classes:可以不用透過include檔案來加載類別,可以透過__autoload()或spl_autoload_register() 函数自動註冊類別.

    ```php
    spl_autoload_register(function ($class_name) {
        require_once $class_name . '.php';
    });
    $obj  = new MyClass1();
    $obj2 = new MyClass2();
    ```

7. Constructors and Destructors,在創建時會先調用__construct,註銷或程序結束時會調用__destruct.

    ```php
    class MyDestructableClass {
       function __construct() {
           print "In constructor\n";
           $this->name = "MyDestructableClass";
       }
       function __destruct() {
           print "Destroying " . $this->name . "\n";
       }
    }
    $obj = new MyDestructableClass();
    unset($obj);
    ```

8. Visibility:包含public、protected、private.

    ```php
    class MyClass
    {
        public $public = 'Public';
        protected $protected = 'Protected';
        private $private = 'Private';
        function printHello()
        {
            echo $this->public;
            echo $this->protected;
            echo $this->private;
        }
    }
    $obj = new MyClass();
    echo $obj->public; //public
    echo $obj->protected; //產生錯誤
    echo $obj->private; //產生錯誤
    $obj->printHello(); //印出Public、Protected和Private
    ```

9. Scope Resolution Operator(::):用於訪問類別的靜態成員、常量或函式.

    ```php
    class MyClass {
        const CONST_VALUE = 'A constant value';
    }
    echo MyClass::CONST_VALUE;
    ```

10. Class Abstraction:繼承抽象類別的子類別,強制要求一定要有父類別定義的抽象函式的實作.這樣的好處是統一子類別中的實作格式.

    ```php
    abstract class AbstractClass
    {
        //抽象方法僅需要定義需要的参数
        abstract protected function prefixName($name);
    }
    class ConcreteClass extends AbstractClass
    {
        //子類別可以定義父類別抽象方法中不存在的可選参数
        public function prefixName($name, $separator = ".") {
            if ($name == "Pacman") {
                $prefix = "Mr";
            } elseif ($name == "Pacwoman") {
                $prefix = "Mrs";
            } else {
                $prefix = "";
            }
            return "{$prefix}{$separator} {$name}";
        }
    }
    $class = new ConcreteClass;
    echo $class->prefixName("Pacman"), "\n"; //Mr. Pacman
    echo $class->prefixName("Pacwoman"), "\n"; //Mrs. Pacwoman
    ```

11. Object Interfaces,透過implements導入多個介面接口,只能定義方法,但不能實作.

    ```php
    interface iTemplate
    {
        public function setVariable($name, $var);
        public function getHtml($template);
    }
    class Template implements iTemplate
    {
        private $vars = array();
        public function setVariable($name, $var)
        {
            $this->vars[$name] = $var;
        }
        public function getHtml($template)
        {
            foreach($this->vars as $name => $value) {
                $template = str_replace('{' . $name . '}', $value, $template);
            }
            return $template;
        }
    }
    ```

12. Class Abstraction(抽象類別)與Object Interfaces(介面)的差異性如下面表格.
    ||類別(Class)|抽象類別(Abstract Class)|介面(Interface)|
    |:---|:---:|:---:|---:|
    |宣告屬性(attribute)|O|O|X|
    |常數(const)|O|O|O|
    |實例化(new class)|O|X|X|
    |抽象方法(abstract function)|X|O|O|
    |實作方法內容(functoin())|O|O|X|
    |類別是否可繼承多個|X|X|O|
13. Trait:自PHP5.4.0起可使用.介於繼承與介面之間的功能,可以參考[Trait][].

    ```php
    trait PrivateTrait
    {
        private privateFunc()
        {
            echo "This is private";
        }
    }
    class PrivateClass
    {
        use privateTrait;
        // This is allowed.
        public publicFunc()
        {
            $this->privateFunc();
        }
    }
    ```

14. Anonymous classes.PHP7開始支持匿名類別.匿名類別可以創建一次性的簡單對象.
15. Overloading:動態創建成員與方法.

    ```php
    public void __set ( string $name , mixed $value )
    public mixed __get ( string $name )
    public bool __isset ( string $name )
    public void __unset ( string $name )

    class PropertyTest {
        private $data = array();
        public $declared = 1;
        private $hidden = 2;
        public function __set($name, $value)
        {
            $this->data[$name] = $value;
        }
        public function __get($name)
        {
            if (array_key_exists($name, $this->data)) {
                return $this->data[$name];
            }
            $trace = debug_backtrace();
            trigger_error(
                'Undefined property via __get(): ' . $name .
                ' in ' . $trace[0]['file'] .
                ' on line ' . $trace[0]['line'],
                E_USER_NOTICE);
            return null;
        }
        public function __isset($name)
        {
            return isset($this->data[$name]);
        }
        public function __unset($name)
        {
            unset($this->data[$name]);
        }
        public function getHidden()
        {
            return $this->hidden;
        }
    }
    $obj = new PropertyTest;
    $obj->a = 1;
    echo $obj->a; //1
    var_dump(isset($obj->a)); //true
    unset($obj->a);
    var_dump(isset($obj->a)); //false
    ```

16. Magic Methods
    * __sleep()
    * __wakeup()
    * __construct()
    * __destruct()
    * __call()
    * __callStatic()
    * __get()
    * __set()
    * __isset()
    * __unset()
    * __sleep()
    * __wakeup()
    * __toString()
    * __invoke()
    * __set_state()
    * __clone()
    * __debugInfo()

[Virtualbox]:https://www.virtualbox.org/
[Vagrant]:https://www.vagrantup.com/
[Trait]:http://oomusou.io/php/php-trait/
