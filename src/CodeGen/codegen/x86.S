.section .rodata
.global main1
CS335_format: .string "%d\n"
f1:
push %rbp
mov %rsp, %rsp
sub $5, %rsp
mov 4, %rax
mov %rbp, %rsp
pop %rbp
ret
main1:
push %rbp
mov %rsp, %rsp
sub $112, %rsp
mov 4, ebx
push ebx
mov 8, ecx
push ecx
call f1
mov %rax, ebx
mov ebx, ecx
mov  -20(%rbp) , edx
mov edx, esi
mov 1, esi
mov  -32(%rbp) , r8
mov r8, r9
mov 0, r9
mov  -32(%rbp) , r10
mov r10, r11
mov 90, r11
mov  -32(%rbp) , r12
mov r12, r13
mov 845, r13
mov 2,r14
mov  -8(%rbp) , r15
push r15
mov r15, r15
mov 4 ,%rax
mov ecx, -12(%rbp)
mov r15, -112(%rbp)
mov $CS335_format, %rdi
mov %rax, %rsi
call printf
