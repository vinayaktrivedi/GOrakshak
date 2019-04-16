.section .rodata
.global main
CS335_format: .string "%d\n"
FibonacciRecursion1:
push %rbp
mov %rsp, %rsp
sub $0, %rsp
mov  --8(%rbp) , %rbx
cmp $1, %rbx
setle %al
movbzl %al, %rax
mov %rax, %rbx
mov %rbx, %rax
cmp %rax, $0
je CS335_4
mov -8, %rax
leave
ret
CS335_4:
mov  --8(%rbp) , %rbx
sub $1, %rbx
push %rbx
call FibonacciRecursion1
mov %rax, %rbx
mov  --8(%rbp) , %rcx
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
mov %rsp, %rsp
sub $4, %rsp
mov  --8(%rbp) , %rbx
sub $1, %rbx
mov %rbx, %rcx
mov -8, %rax
mov %rcx, -4(%rbp)
leave
ret
mov 4, %rax
leave
ret
main:
push %rbp
mov %rsp, %rsp
sub $12, %rsp
push $19
call FibonacciRecursion1
mov %rax, %rbx
mov %rbx, %rcx
push $10
mov %rcx, -4(%rbp)
call foo1
mov %rax, %rbx
mov %rax, %rcx
mov %rbx, %rdx
mov %rcx, %rsi
