.section .rodata
.global main
CS335_format: .string "%d\n"
FibonacciRecursion1:
push %rbp
mov %rsp, %rbp
sub $0, %rsp
mov  16(%rbp) , %rbx
mov %rbx, %rax
cmp %rax, $0
je CS335_4
mov 16, %rax
leave
ret
CS335_4:
mov  16(%rbp) , %rbx
sub $1, %rbx
push %rbx
call FibonacciRecursion1
mov %rax, %rbx
mov  16(%rbp) , %rcx
sub $2, %rcx
push %rcx
call FibonacciRecursion1
mov %rax, %rbx
push %rcx
add %rbx, %rcx
mov %rcx, %rax
leave
ret
foo1:
push %rbp
mov %rsp, %rbp
sub $8, %rsp
mov  16(%rbp) , %rbx
sub $1, %rbx
mov %rbx, %rcx
mov 16, %rax
mov %rcx, -8(%rbp)
leave
ret
mov -8, %rax
leave
ret
main:
push %rbp
mov %rsp, %rbp
sub $24, %rsp
push $5
call FibonacciRecursion1
mov %rax, %rbx
mov %rbx, %rcx
mov %rcx, %rax
mov %rcx, -8(%rbp)
mov $CS335_format, %rdi
mov %rax, %rsi
mov $0, %rax
call printf
<<<<<<< HEAD
push $10
=======
mov $0, %rax
>>>>>>> e0d84456528e4b416ab855885d576d96a499baea
leave
ret
main:
push %rbp
mov %rsp, %rbp
sub $24, %rsp
push $19
call FibonacciRecursion1
mov %rax, %rbx
mov %rbx, %rcx
push $10
mov %rcx, -8(%rbp)
>>>>>>> bc2856f1906af36e5c7abd27fca9c92987b7152b
call foo1
mov %rax, %rbx
mov %rax, %rcx
mov %rbx, %rdx
mov %rcx, %rsi
