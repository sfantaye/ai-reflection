'use client'

import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { ThemeToggle } from './theme-toggle'
import { Menu } from 'lucide-react'
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
} from '@/components/ui/dropdown-menu'

export function Navbar() {
  return (
    <nav className="fixed top-0 z-50 rounded-b-[2em] w-full bg-white/80 dark:bg-black/80 backdrop-blur-md border-b border-orange-500">
      <div className="max-w-2xl mx-auto px-4 py-4 sm:py-5 flex items-center justify-between">
        {/* Site Title / Logo */}
        <Link href="/" className="text-xl font-semibold tracking-tight">
          <span className="inline-flex items-center gap-2">
            <span className="sm:hidden">AI-<span className="text-orange-500">R</span></span>
            <span className="hidden sm:inline">AI <span className="text-orange-500">Reflection</span></span>
          </span>
        </Link>

        {/* Desktop Navigation */}
        <div className="hidden sm:flex items-center gap-2">
          <Link href="/about">
            <Button variant="ghost">About</Button>
          </Link>
          <Link href="/contact">
            <Button variant="ghost">Contact</Button>
          </Link>
          <ThemeToggle />
        </div>

        {/* Mobile Navigation */}
        <div className="sm:hidden flex items-center gap-1">
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
  )
}