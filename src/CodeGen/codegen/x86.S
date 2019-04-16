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
mov ebx, --8[ebp]
cmp ebx, 1
setle al
movbzl eax, al
mov ebx, eax
mov eax,ebx
cmp 0, eax
je CS335_4
mov eax,-8
ret
CS335_4:
mov ebx, --8[ebp]
sub ebx, 1
push ebx
call FibonacciRecursion1
mov ebx, eax
mov ecx, --8[ebp]
sub ecx, 2
push ecx
call FibonacciRecursion1
mov ebx, eax
push ecx
add ecx, ebx
mov eax,ecx
ret
foo1:
push rbp
mov rbp, rsp
push eax
push ebx
push esi
push edi
push edx
mov ebx, --8[ebp]
sub ebx, 1
mov ecx, ebx
mov eax,-8
mov -4[ebp],ecx
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
mov ebx, eax
mov ecx, ebx
push 10
mov -4[ebp],ecx
call foo1
mov ebx, eax
mov ecx, eax
mov edx, ebx
mov esi, ecx
