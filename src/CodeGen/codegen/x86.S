.section .rodata
.global main
CS335_format: .string "%d\n"
f1:
push %rbp
mov %rsp, %rbp
sub $0, %rsp
mov  -8(%rbp) , %rbx
mov 12(%rbp), %rcx
add %rcx, %rbx
mov %rbx, %rax
leave
ret
main:
push %rbp
mov %rsp, %rbp
sub $12, %rsp
mov $10,%rbx
mov $90,%rcx
push %rbx
push %rcx
mov %rbx, --4(%rbp) a
mov %rcx, --8(%rbp) b
call f1
mov %rax, %rbx
mov %rbx, %rcx
mov %rcx, %rax
mov %rcx, --12(%rbp) c
mov $CS335_format, %rdi
mov %rax, %rsi
mov $0, %rax
call printf
mov $0, %rax
leave
ret
