import React from 'react';
import './Input.css';

export const Input = ({
  label,
  error,
  success,
  helperText,
  icon,
  iconPosition = 'left',
  required = false,
  fullWidth = false,
  className = '',
  ...props
}) => {
  const inputGroupClasses = [
    'input-group',
    fullWidth && 'input-group-full',
    className
  ].filter(Boolean).join(' ');

  const inputWrapperClasses = [
    'input-wrapper',
    icon && 'input-with-icon',
    icon && `input-icon-${iconPosition}`,
    error && 'input-wrapper-error',
    success && 'input-wrapper-success',
    props.disabled && 'input-wrapper-disabled'
  ].filter(Boolean).join(' ');

  return (
    <div className={inputGroupClasses}>
      {label && (
        <label className={`input-label ${required ? 'input-label-required' : ''}`}>
          {label}
        </label>
      )}

      <div className={inputWrapperClasses}>
        {icon && iconPosition === 'left' && (
          <span className="input-icon input-icon-left">
            {icon}
          </span>
        )}

        <input
          className="input"
          {...props}
        />

        {icon && iconPosition === 'right' && (
          <span className="input-icon input-icon-right">
            {icon}
          </span>
        )}
      </div>

      {error && (
        <span className="input-message input-error-message">
          {error}
        </span>
      )}

      {!error && helperText && (
        <span className="input-message input-helper-text">
          {helperText}
        </span>
      )}
    </div>
  );
};

export const Textarea = ({
  label,
  error,
  helperText,
  required = false,
  fullWidth = false,
  rows = 4,
  className = '',
  ...props
}) => {
  const inputGroupClasses = [
    'input-group',
    fullWidth && 'input-group-full',
    className
  ].filter(Boolean).join(' ');

  const textareaClasses = [
    'input',
    'textarea',
    error && 'input-error'
  ].filter(Boolean).join(' ');

  return (
    <div className={inputGroupClasses}>
      {label && (
        <label className={`input-label ${required ? 'input-label-required' : ''}`}>
          {label}
        </label>
      )}

      <textarea
        className={textareaClasses}
        rows={rows}
        {...props}
      />

      {error && (
        <span className="input-message input-error-message">
          {error}
        </span>
      )}

      {!error && helperText && (
        <span className="input-message input-helper-text">
          {helperText}
        </span>
      )}
    </div>
  );
};
