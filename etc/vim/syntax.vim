" Vim syntax file
" Language:    HLDS
" Maintainer:  Zeus WPI

" quit when a syntax file was already loaded.
if exists("b:current_syntax")
	finish
endif

" We need nocompatible mode in order to continue lines with backslashes.
" Original setting will be restored.
let s:cpo_save = &cpo
set cpo&vim

syn match hldsLocationAttribute "^\t[a-z0-9_-]\+ " display contained nextgroup=hldsLocationAttributeValue
syn match hldsLocationAttributeValue "[^\n]\+$" display contained

syn region  hldsLocationHeader matchgroup=hldsLocationHeaderDelim
	\ start="^====*$" end="^====*$"
	\ contains=hldsLocationAttribute,hldsComment

syn keyword hldsBlockType     dish                       nextgroup=hldsBlockIdAftrKywrd skipwhite
syn keyword hldsChoiceType    single_choice multi_choice nextgroup=hldsBlockIdAftrKywrd skipwhite

syn match   hldsBlockId          "^[a-z0-9_-]\+: "
syn match   hldsBlockIdAftrKywrd "[a-z0-9_-]\+: " contained

syn match   _doubleSpace  "  \+" nextgroup=hldsTag,hldsPrice
syn match   hldsTag       "{[a-z0-9_-]\+}\( \|$\)"            contained nextgroup=hldsTag,hldsPrice
syn match   hldsPrice     "€ *[0-9]\+\(\.[0-9]\+\|\)\( \|$\)" contained

syn match   hldsComment       "#.*$" contains=hldsTodo,@Spell
syn keyword hldsTodo          FIXME NOTE NOTES TODO XXX contained

" trailing whitespace
syn match   hldsSpaceError    display excludenl "\s\+$"
" spaces instead of tabs
syn match   hldsSpaceError    display "^\t* "

" The default highlight links.  Can be overridden later.
hi def link hldsLocationHeader      Function
hi def link hldsLocationHeaderDelim hldsLocationHeader
hi def link hldsLocationAttribute   hldsLocationHeader
hi def link hldsChoiceType          Statement
hi def link hldsBlockType           Statement
hi def link hldsBlockId             Include
hi def link hldsBlockIdAftrKywrd    hldsBlockId
hi def link hldsPrice               Number
hi def link hldsTag                 String
hi def link hldsSpaceError          Error
hi def link hldsComment             Comment
hi def link hldsTodo                Todo

syntax sync minlines=5

let b:current_syntax = "hlds"

let &cpo = s:cpo_save
unlet s:cpo_save
