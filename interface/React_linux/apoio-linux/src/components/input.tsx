import React from "react";
import "./input.css";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  className?: string;
}

export const Input: React.FC<InputProps> = ({ className = "", ...props }) => {
  return <input className={`question-input ${className}`} {...props} />;
};
