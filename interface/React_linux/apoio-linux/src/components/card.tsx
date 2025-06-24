import React from "react";
import "./card.css";

interface CardProps {
  text: string;
  onGenerate?: (text: string) => void; // nova prop opcional
}

export const Card: React.FC<CardProps> = ({ text, onGenerate }) => {
  return (
    <div className="card">
      <div className="card-content">
        <div className="icon">
          <img src="/Seta.svg" alt="seta" className="icon-svg" />
        </div>
        <p className="card-title">Sugestão de prompt</p>
        <p className="card-text">{text}</p>
        {onGenerate && (
          <button className="generate" onClick={() => onGenerate(text)}>
            Gerar resposta
          </button>
        )}
      </div>
    </div>
  );
};
