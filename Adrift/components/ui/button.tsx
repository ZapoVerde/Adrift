import React from 'react';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  className?: string;
  children: React.ReactNode;
}

/**
 * A basic Tailwind-styled button.
 */
export const Button: React.FC<ButtonProps> = ({
  children,
  className = '',
  ...props
}) => (
  <button
    className={[
      'px-4 py-2',
      'bg-blue-600 text-white',
      'rounded hover:bg-blue-700',
      'focus:outline-none focus:ring-2 focus:ring-blue-500',
      className
    ].join(' ')}
    {...props}
  >
    {children}
  </button>
);
