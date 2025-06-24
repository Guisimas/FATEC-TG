import React from "react";
import ReactMarkdown from "react-markdown";
import "./resposta.css";

interface RespostaProps {
  pergunta: string;
  resposta: string;
}

export const Resposta: React.FC<RespostaProps> = ({ pergunta, resposta }) => {
  return (
    <div className="resposta-container">
      <div className="resposta-card">
        <h2 className="resposta-title">Pergunta</h2>
        <p className="resposta-pergunta">{pergunta}</p>

        <h2 className="resposta-title">Resposta</h2>
        <div className="resposta-markdown">
          <ReactMarkdown>{resposta}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
};
