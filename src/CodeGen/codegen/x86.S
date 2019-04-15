section	.text
global _start
f1:
push rbp
mov rbp, rsp
push eax
push ebx
push esi
push edi
push edx
mov rbx, 3
mov eax,rbx
mov -8[ebp],rbx
ret
main1:
push rbp
mov rbp, rsp
push eax
push ebx
push esi
push edi
push edx
mov rbx, 10
mov rcx, 19
push rbx
push rcx
mov -4[ebp],rbx
mov -8[ebp],rcx
call f1
mov rbx, eax
mov rcx -4[ebp]
