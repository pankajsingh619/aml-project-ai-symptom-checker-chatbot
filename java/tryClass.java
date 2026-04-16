// File: java/try.java
public class tryClass{
    public static void Main(String []args){
int a[] = new int[5];
System.out.println("Hello Guys");
try{
    System.out.println(a[7]);
}
catch(ArrayIndexOutOfBoundsException e){
    // Handle the exception here if needed
    system.out.println("out of bound ");

}
    System.out.println("byeee");
    }
}
