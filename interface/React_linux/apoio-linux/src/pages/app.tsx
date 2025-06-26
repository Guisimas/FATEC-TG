import { useState } from "react";
import ReactMarkdown from "react-markdown";
import "@pages/app.css";
import { Button } from "@components/button";
import { Card } from "@components/card";
import { Input } from "@components/input";
import { useNavigate } from "react-router-dom";

interface CardData {
  text: string;
}

export default function App() {
  const navigate = useNavigate();
  const [question, setQuestion] = useState<string>("");
  const [answer, setAnswer] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [hasStarted, setHasStarted] = useState(false);

  const cards: CardData[] = [
    {
      text: "Qual a diferença entre os comandos chmod, chown e chgrp? Dê exemplos.",
    },
    {
      text: "Como posso verificar quais processos estão consumindo mais CPU e memória no meu sistema Linux?",
    },
    {
      text: "Quais arquivos são lidos durante a inicialização do Linux e qual é a ordem de execução?",
    },
  ];

  const handleSend = async (pergunta: string) => {
    if (!pergunta.trim()) return;

    setHasStarted(true);
    setLoading(true);
    setAnswer(null);
    setQuestion(pergunta);

    try {
      const res = await fetch("http://34.56.148.46:8000/pergunta", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pergunta }),
      });

      const data = await res.json();
      setAnswer(data.resposta);
    } catch (error) {
      setAnswer("Ocorreu um erro ao buscar a resposta.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div>
          <div className="logo">
            <img src="/Logo.svg" alt="Professor Virtual" className="logo-icon" />
          </div>
          <Button
            className="new-chat"
            onClick={() => {
              setAnswer(null);
              setQuestion("");
              setHasStarted(false);
            }}
          >
            + Novo chat
          </Button>
           <Button
            className="prompt-design-button"
            onClick={() => navigate("/prompt-design")}
          >
            Prompt Design
          </Button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main">
        {!hasStarted && <h1 className="title">Olá! O que gostaria de estudar hoje? 👋</h1>}

        {!hasStarted && (
          <div className="cards">
            {cards.map((card, index) => (
              <Card key={index} text={card.text} onGenerate={handleSend} />
            ))}
          </div>
        )}

        {loading && <p className="loading-message">Buscando resposta...</p>}

        {answer && (
          <div className="answer markdown-body fade-in">
            <ReactMarkdown>{answer}</ReactMarkdown>
          </div>
        )}

        <div className="input-wrapper">
          <Input
            placeholder="Qual a sua dúvida?"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
          <button className="send-button" onClick={() => handleSend(question)}>
            <img src="/send.svg" alt="Enviar" />
          </button>
        </div>
      </main>
    </div>
  );
}
