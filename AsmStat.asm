include 'emu8086.inc'

.model small
.stack 100h

.data
    ; --- Massive ASCII Art and Menu Banner ---
    banner      db "       _                 ____  _        _   ", 13, 10
                db "      / \   ___ _ __ ___/ ___|| |_ __ _| |_ ", 13, 10
                db "     / _ \ / __| '_ ` _ \___ \| __/ _` | __|", 13, 10
                db "    / ___ \\__ \ | | | | |___) | || (_| | |_ ", 13, 10
                db "   /_/   \_\___/_| |_| |_|____/ \__\__,_|\__|", 13, 10
                db 13, 10
                db "  ===========================================", 13, 10
                db "  ||        SELECT A MATH OPERATION        ||", 13, 10
                db "  ===========================================", 13, 10
                db "  ||                                       ||", 13, 10
                db "  ||  [1] Input Array Data                 ||", 13, 10
                db "  ||  [2] Show Array                       ||", 13, 10
                db "  ||  [3] Sum & Mean                       ||", 13, 10
                db "  ||  [4] Variance (Integer)               ||", 13, 10
                db "  ||  [5] Bubble Sort Array                ||", 13, 10
                db "  ||  [6] Median (Run Sort first)          ||", 13, 10
                db "  ||  [7] Min & Max                        ||", 13, 10
                db "  ||  [8] Exit Program                     ||", 13, 10
                db "  ||                                       ||", 13, 10
                db "  ===========================================", 13, 10
                db 13, 10
                db "  Enter choice: $"
                
    ; --- Prompt Strings ---
    prompt_len  db 13, 10, "Enter number of elements (1-20): $"
    prompt_ele  db 13, 10, "Enter element: $"
    msg_sum     db 13, 10, "Sum: $"
    msg_mean    db 13, 10, "Mean: $"
    msg_var     db 13, 10, "Variance (Integer): $"
    msg_med     db 13, 10, "Median: $"
    msg_min     db 13, 10, "Min: $"
    msg_max     db 13, 10, "Max: $"
    msg_sort    db 13, 10, "Array successfully sorted!$"
    msg_arr     db 13, 10, "Array: $"
    msg_empty   db 13, 10, "Error: Array is empty. Please select Option 1 first.$"
    msg_space   db " $"
    msg_pause   db 13, 10, 13, 10, "Press any key to return to menu...$"
    msg_done    db 13, 10, "Data Loaded & Synced to Web App (DATA.TXT)!$"
    
    ; --- File Export Variables ---
    filename    db 'DATA.TXT', 0
    file_handle dw ?
    file_buffer db 256 dup(0)
    
    ; --- Variables ---
    array       dw 20 dup(0)    ; Reserve space for up to 20 16-bit integers
    arr_len     dw 0            ; Store the actual number of elements entered
    
.code
main proc
    mov ax, @data
    mov ds, ax          ; Initialize data segment

menu_loop:
    lea dx, banner  ; uper wala menu text ka address dx mn stored
    
    mov ah, 09h
    int 21h

    call scan_num       ; User input is stored in CX
    
    cmp cx, 1
    je do_input
    cmp cx, 2
    je do_show
    cmp cx, 3
    je do_sum_mean
    cmp cx, 4
    je do_variance
    cmp cx, 5
    je do_sort
    cmp cx, 6
    je do_median
    cmp cx, 7
    je do_min_max
    cmp cx, 8
    je exit_prog
    jmp menu_loop

; --- MENU HANDLERS ---
do_input:
    call input_array
    lea dx, msg_done
    mov ah, 09h
    int 21h
    jmp pause_and_menu

do_show:
    call show_array
    jmp pause_and_menu

do_sum_mean:
    call check_empty
    cmp ax, 0
    je pause_and_menu
    call asm_sum
    push ax
    lea dx, msg_sum
    mov ah, 09h
    int 21h
    pop ax
    call print_num
    call asm_mean
    push ax
    lea dx, msg_mean
    mov ah, 09h
    int 21h
    pop ax
    call print_num
    jmp pause_and_menu

do_variance:
    call check_empty
    cmp ax, 0
    je pause_and_menu
    call asm_variance
    push ax
    lea dx, msg_var
    mov ah, 09h
    int 21h
    pop ax
    call print_num
    jmp pause_and_menu

do_sort:
    call check_empty
    cmp ax, 0
    je pause_and_menu
    call bubble_sort
    lea dx, msg_sort
    mov ah, 09h
    int 21h
    jmp pause_and_menu

do_median:
    call check_empty
    cmp ax, 0
    je pause_and_menu
    call asm_median
    push ax
    lea dx, msg_med
    mov ah, 09h
    int 21h
    pop ax
    call print_num
    jmp pause_and_menu

do_min_max:
    call check_empty
    cmp ax, 0
    je pause_and_menu
    call asm_min
    push ax
    lea dx, msg_min
    mov ah, 09h
    int 21h
    pop ax
    call print_num
    call asm_max
    push ax
    lea dx, msg_max
    mov ah, 09h
    int 21h
    pop ax
    call print_num
    jmp pause_and_menu

pause_and_menu:
    lea dx, msg_pause
    mov ah, 09h
    int 21h
    mov ah, 00h
    int 16h
    jmp menu_loop

exit_prog:
    mov ah, 4ch
    int 21h
main endp

;-----------------------------------------
; UTILITY: Checks if array is empty
check_empty proc
    cmp arr_len, 0
    je is_empty
    mov ax, 1
    ret
is_empty:
    lea dx, msg_empty
    mov ah, 09h
    int 21h
    mov ax, 0
    ret
check_empty endp

;-----------------------------------------
; PROCEDURE 1: Input Array
input_array proc
    lea dx, prompt_len
    mov ah, 09h
    int 21h
    call scan_num
    mov arr_len, cx
    lea si, array
    mov bx, cx
input_loop:
    lea dx, prompt_ele
    mov ah, 09h
    int 21h
    call scan_num
    mov [si], cx
    add si, 2
    dec bx
    jnz input_loop
    
    call export_array       ; Sync to DATA.TXT
    
    ret
input_array endp

;-----------------------------------------
; PROCEDURE: Export Array to DATA.TXT
;-----------------------------------------
export_array proc
    push ax
    push bx
    push cx
    push dx
    push si
    push di

    ; 1. Create File DATA.TXT
    mov ah, 3Ch
    mov cx, 0               ; Normal attributes
    lea dx, filename
    int 21h
    jc export_done          ; If error, silently exit
    mov file_handle, ax

    ; 2. Convert Array to String in file_buffer
    lea di, array
    mov cx, arr_len
    lea si, file_buffer
export_loop:
    mov ax, [di]
    call num_to_str
    
    ; Add comma and space if not last element
    cmp cx, 1
    je export_skip_comma
    mov byte ptr [si], ','
    inc si
    mov byte ptr [si], ' '
    inc si
export_skip_comma:
    add di, 2               ; Move to next element in array
    dec cx
    jnz export_loop

    ; 3. Write Buffer to File
    mov cx, si
    lea dx, file_buffer
    sub cx, dx              ; CX = number of bytes to write
    mov ah, 40h
    mov bx, file_handle
    int 21h

    ; 4. Close File
    mov ah, 3Eh
    mov bx, file_handle
    int 21h

export_done:
    pop di
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
export_array endp

;-----------------------------------------
; UTILITY: Convert Number in AX to String in Buffer
; Input: AX = number, SI = buffer pointer
; Returns: SI = updated buffer pointer
;-----------------------------------------
num_to_str proc
    push ax
    push bx
    push cx
    push dx

    mov cx, 0
    mov bx, 10
nts_loop1:
    xor dx, dx
    div bx
    push dx                 ; Push remainder onto stack
    inc cx
    test ax, ax
    jnz nts_loop1

nts_loop2:
    pop dx                  ; Pop remainder
    add dl, '0'             ; Convert to ASCII
    mov [si], dl            ; Store in buffer
    inc si
    loop nts_loop2

    pop dx
    pop cx
    pop bx
    pop ax
    ret
num_to_str endp

;-----------------------------------------
; PROCEDURE 2: Show Array
show_array proc
    call check_empty
    cmp ax, 0
    je show_done
    lea dx, msg_arr
    mov ah, 09h
    int 21h
    lea si, array
    mov cx, arr_len
show_loop:
    mov ax, [si]
    call print_num
    lea dx, msg_space
    mov ah, 09h
    int 21h
    add si, 2
    loop show_loop
show_done:
    ret
show_array endp

;-----------------------------------------
; PROCEDURE: Sum
asm_sum proc
    lea si, array
    mov cx, arr_len
    xor ax, ax
sum_loop:
    add ax, [si]
    add si, 2
    loop sum_loop
    ret
asm_sum endp

;-----------------------------------------
; PROCEDURE: Mean
asm_mean proc
    call asm_sum
    xor dx, dx
    mov bx, arr_len
    div bx
    ret
asm_mean endp

;-----------------------------------------
; PROCEDURE: Variance
asm_variance proc
    call asm_mean
    mov bx, ax
    lea si, array
    mov cx, arr_len
    xor di, di
var_loop:
    mov ax, [si]
    sub ax, bx
    imul ax
    add di, ax
    add si, 2
    loop var_loop
    mov ax, di
    xor dx, dx
    mov bx, arr_len
    div bx
    ret
asm_variance endp

;-----------------------------------------
; PROCEDURE: Bubble Sort (O(N^2))
; Modifies array in memory
;-----------------------------------------
bubble_sort proc
    mov cx, arr_len
    dec cx              ; CX = N - 1 (Number of passes)
    jz sort_done        ; If N=1, it's already sorted
    
outer_loop:
    push cx             ; Save outer loop counter
    lea si, array       ; Reset pointer to start of array
inner_loop:
    mov ax, [si]        ; Load current element
    mov bx, [si+2]      ; Load next element
    cmp ax, bx          ; Compare them
    jle no_swap         ; If current <= next, do nothing
    
    ; Perform Swap
    mov [si], bx        ; Put smaller number in current slot
    mov [si+2], ax      ; Put larger number in next slot
    
no_swap:
    add si, 2           ; Move to next adjacent pair
    loop inner_loop     ; End of inner loop
    
    pop cx              ; Restore outer loop counter
    loop outer_loop     ; End of outer loop
sort_done:
    ret
bubble_sort endp

;-----------------------------------------
; PROCEDURE: Median (Assumes array is sorted)
; Returns: AX = Median
;-----------------------------------------
asm_median proc
    mov ax, arr_len
    shr ax, 1           ; AX = N / 2
    mov bx, ax
    shl bx, 1           ; Multiply by 2 for byte offset
    lea si, array
    add si, bx          ; SI now points to middle of array
    
    mov ax, arr_len
    test ax, 1          ; Check if N is odd or even
    jnz is_odd
    
is_even:
    ; For even arrays, median is average of two middle elements
    mov ax, [si]        ; Middle right
    mov bx, [si-2]      ; Middle left
    add ax, bx
    shr ax, 1           ; Divide by 2
    ret
    
is_odd:
    ; For odd arrays, median is just the exact middle element
    mov ax, [si]
    ret
asm_median endp

;-----------------------------------------
; PROCEDURE: Find Minimum
; Returns: AX = Min
;-----------------------------------------
asm_min proc
    lea si, array
    mov cx, arr_len
    mov ax, [si]        ; Assume first element is min
    add si, 2
    dec cx
    jz min_done
min_loop:
    cmp ax, [si]
    jle min_skip
    mov ax, [si]        ; Update min
min_skip:
    add si, 2
    loop min_loop
min_done:
    ret
asm_min endp

;-----------------------------------------
; PROCEDURE: Find Maximum
; Returns: AX = Max
;-----------------------------------------
asm_max proc
    lea si, array
    mov cx, arr_len
    mov ax, [si]        ; Assume first element is max
    add si, 2
    dec cx
    jz max_done
max_loop:
    cmp ax, [si]
    jge max_skip
    mov ax, [si]        ; Update max
max_skip:
    add si, 2
    loop max_loop
max_done:
    ret
asm_max endp

; --- EMU8086 STANDARD INCLUDES ---
DEFINE_SCAN_NUM
DEFINE_PRINT_NUM
DEFINE_PRINT_NUM_UNS
end main
