;
; Copyright (c) 2011 Nokia Corporation and/or its subsidiary(-ies).
; All rights reserved.
; This component and the accompanying materials are made available
; under the terms of the License "Eclipse Public License v1.0"
; which accompanies this distribution, and is available
; at the URL "http://www.eclipse.org/legal/epl-v10.html".
;
; Initial Contributors:
; Nokia Corporation - initial contribution.
;
; Contributors:
;
; Description: 
;
        AREA |.text|, CODE, READONLY, ALIGN=6

        CODE32

        ; UPT

;
;



;EXPORT fake_assembler_function1
        EXPORT  _Z24fake_assembler_function2v

;fake_assembler_function1
_Z24fake_assembler_function2v
        mov             r0,r0           ; nop
        mov             r0,r0           ; nop
        mov             r0,r0           ; nop
        mov             r0,r0           ; nop
        mov             r0,r0           ; nop
        mov             r0,r0           ; nop
        mov             r0,r0           ; nop
        mov             r0,r0           ; nop
        mov             r0,r0           ; nop
        mov             r0,r0           ; nop
        mov             r0,r0           ; nop
        mov             r0,r0           ; nop
        mov             r0,r0           ; nop
        mov             r0,r0           ; nop
        mov             r0,r0           ; nop
        mov             r0,r0           ; nop
        mov             r0,r0           ; nop
        mov             r0,r0           ; nop
        mov             r0,r0           ; nop
        bx lr

        END

; End of file - asm2.s

