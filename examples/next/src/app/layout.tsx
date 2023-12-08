'use client';

import { Providers } from '@openassistants/ui';
import "@openassistants/ui/globals.css"

interface RootLayoutProps {
  children: React.ReactNode;
}

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <Providers defaultTheme="light" disableTransitionOnChange>
          <main className="flex h-full flex-col flex-1 bg-muted/50">{children}</main>
        </Providers>
      </body>
    </html>
  );
}
