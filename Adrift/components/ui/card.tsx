import React from 'react';

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  className?: string;
}

/**
 * A simple container with border, shadow, and rounded corners.
 */
export const Card: React.FC<CardProps> = ({
  children,
  className = '',
  ...props
}) => (
  <div
    className={[
      'bg-white',
      'border border-gray-200',
      'shadow rounded-lg',
      className
    ].join(' ')}
    {...props}
  >
    {children}
  </div>
);

/**
 * Header section of a Card. Typically holds a title.
 */
export const CardHeader: React.FC<CardProps> = ({
  children,
  className = '',
  ...props
}) => (
  <div
    className={[
      'px-4 py-2',
      'border-b border-gray-100',
      'font-semibold',
      className
    ].join(' ')}
    {...props}
  >
    {children}
  </div>
);

/**
 * Main content area of a Card.
 */
export const CardContent: React.FC<CardProps> = ({
  children,
  className = '',
  ...props
}) => (
  <div className={['p-4', className].join(' ')} {...props}>
    {children}
  </div>
);
