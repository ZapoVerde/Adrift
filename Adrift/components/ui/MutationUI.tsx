import React from 'react';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  /**
   * Custom styling classes to apply on top of variant and size defaults
   */
  className?: string;
  /**
   * Contents to render inside the button
   */
  children: React.ReactNode;
  /**
   * Visual style variant:
   * - 'default': solid filled button
   * - 'outline': transparent background with border
   */
  variant?: 'default' | 'outline';
  /**
   * Size style:
   * - 'default': regular padding
   * - 'icon': compact padding for icon-only buttons
   */
  size?: 'default' | 'icon';
}

/**
 * A versatile button component with variant and size options.
 * - `variant='outline'` renders a bordered, transparent button.
 * - `size='icon'` applies compact padding for icon use.
 */
export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'default',
  size = 'default',
  className = '',
  ...props
}) => {
  // Base classes common to all variants and sizes
  const classes = [
    'rounded',
    'focus:outline-none',
    'focus:ring-2',
    'focus:ring-blue-500'
  ];

  // Variant-specific classes
  if (variant === 'outline') {
    classes.push(
      'bg-transparent',
      'border',
      'border-gray-300',
      'text-gray-700',
      'hover:bg-gray-100'
    );
  } else {
    classes.push(
      'bg-blue-600',
      'text-white',
      'hover:bg-blue-700'
    );
  }

  // Size-specific classes
  if (size === 'icon') {
    classes.push('p-2');
  } else {
    classes.push('px-4', 'py-2');
  }

  // Append any user-specified classes
  if (className) {
    classes.push(className);
  }

  return (
    <button className={classes.join(' ')} {...props}>
      {children}
    </button>
  );
};
