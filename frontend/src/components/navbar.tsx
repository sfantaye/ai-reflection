'use client'

import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { ThemeToggle } from './theme-toggle'
import { Menu } from 'lucide-react'
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem
} from '@/components/ui/dropdown-menu'
import {
  Tooltip,
  TooltipTrigger,
  TooltipContent,
  TooltipProvider
} from '@/components/ui/tooltip'

export function Navbar() {
  return (
    <TooltipProvider>
      <nav className="w-1/2 mx-auto border-b border-orange-500 rounded-b-[2em] bg-background shadow-sm">
        <div className="px-4 py-5 flex items-center justify-between">
          {/* Site Icon + Title */}
          <Link href="/" className="text-xl font-semibold tracking-tight">
            <span className="inline-flex items-center gap-2">
              <span className="sm:hidden">AI-R</span>
              <span className="hidden sm:inline">AI Reflection</span>
            </span>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden sm:flex items-center gap-2">
            <Tooltip>
              <TooltipTrigger asChild>
                  <Button variant="ghost">About</Button>
              </TooltipTrigger>
              <TooltipContent side="bottom">By Sintayehu Fantaye</TooltipContent>
            </Tooltip>

            <Tooltip>
              <TooltipTrigger asChild>
                  <Button variant="ghost">Contact</Button>
              </TooltipTrigger>
              <TooltipContent side="bottom">Wait! Big thing is coming</TooltipContent>
            </Tooltip>

            <ThemeToggle />
          </div>

          {/* Mobile Menu */}
          <div className="sm:hidden flex items-center gap-2">
            <ThemeToggle />
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon">
                  <Menu className="h-5 w-5" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem asChild>
                  <Link href="/about">About</Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link href="/contact">Contact</Link>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>
      </nav>
    </TooltipProvider>
  )
}
