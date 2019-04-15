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
mov rbx,4
push rbx
mov rcx,8
push rcx
call f1
mov rbx, eax
mov rcx, rbx
mov -4[ebp],rcx
