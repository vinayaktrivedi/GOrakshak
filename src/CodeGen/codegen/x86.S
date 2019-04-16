.section .rodata
.global hello
hello: .string hello world
f1:
push rbp
mov rbp, rsp
push eax
push ebx
push esi
push edi
push edx
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
mov ebx,4
push ebx
mov ecx,8
push ecx
call f1
mov ebx, eax
mov ecx, ebx
mov edx, -20[ebp]
mov esi, edx
mov esi, 1
mov r8, -32[ebp]
mov r9, r8
mov r9, 0
mov r10, -32[ebp]
mov r11, r10
mov r11, 90
mov r12, -32[ebp]
mov r13, r12
mov r13, 845
mov r14, 2
mov r15, -8[ebp]
push r15
mov r15, r15
