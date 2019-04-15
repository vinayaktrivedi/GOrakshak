.section .rodata
.global hello
hello: .string hello world
FibonacciRecursion1:
push rbp
mov rbp, rsp
push eax
push ebx
push esi
push edi
push edx
mov rbx, --8[ebp]
cmp rbx, 1
setle al
movbzl eax, al
mov rbx, eax
mov eax,rbx
cmp 0, eax
je CS335_4
mov eax,-8
ret
CS335_4:
mov rbx, --8[ebp]
sub rbx, 1
push rbx
call FibonacciRecursion1
mov rbx, eax
mov rcx, --8[ebp]
sub rcx, 2
push rcx
call FibonacciRecursion1
mov rbx, eax
push rcx
add rcx, rbx
mov eax,rcx
ret
foo1:
push rbp
mov rbp, rsp
push eax
push ebx
push esi
push edi
push edx
mov rbx, --8[ebp]
sub rbx, 1
mov rcx, rbx
mov eax,-8
mov -4[ebp],rcx
ret
mov eax,4
ret
main1:
push rbp
mov rbp, rsp
push eax
push ebx
push esi
push edi
push edx
push 19
call FibonacciRecursion1
mov rbx, eax
mov rcx, rbx
push 10
mov -4[ebp],rcx
call foo1
mov rbx, eax
mov rcx, eax
mov rdx, rbx
mov rsi, rcx
