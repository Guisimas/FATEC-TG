import React from "react";
import { useNavigate } from "react-router-dom";
import "./promptDesign.css";

export default function PromptDesign() {
  const navigate = useNavigate();

  return (
    <div className="prompt-page">
      <header className="prompt-header">
        <button className="back-button" onClick={() => navigate(-1)}>
          ← Voltar
        </button>
        <h1 className="page-title">Prompt Design Linux</h1>
      </header>

      <main className="prompt-content">
        <section>
          <h2>Auxílio para criar prompts sobre Linux</h2>
          <p>
            Este menu tem como objetivo ajudar você a formular perguntas claras e eficientes
            para obter respostas precisas sobre Linux.
          </p>
        </section>

        <hr />

        <section>
          <h3>1. Seja específico no que você quer saber</h3>
          <ul>
            <li>Evite perguntas vagas, que dificultam o entendimento.</li>
          </ul>
          <blockquote>Como usar o Linux?</blockquote>
          <p>Prefira perguntas que apontem uma dúvida ou problema claro:</p>
          <blockquote>Como listar arquivos ocultos no terminal do Linux?</blockquote>
          <blockquote>Como criar um usuário com permissões limitadas no Debian 11?</blockquote>
        </section>

        <hr />

        <section>
          <h3>2. Dê contexto suficiente</h3>
          <ul>
            <li>Informe o ambiente (distro, versão, shell, etc).</li>
            <li>Explique o que já tentou e o resultado.</li>
          </ul>
          <blockquote>No Ubuntu 20.04, usei <code>apt install nginx</code>, mas o serviço não inicia.</blockquote>
          <blockquote>No Fedora 36, configurei o <code>/etc/hosts</code>, mas o nome não resolve.</blockquote>
        </section>

        <hr />

        <section>
          <h3>3. Use exemplos, comandos e mensagens de erro</h3>
          <p>Incluir comandos e mensagens de erro ajuda na análise:</p>
          <blockquote>Comando: <code>ls -la /var/www</code></blockquote>
          <blockquote>Erro: <code>ls: cannot access '/var/www': Permission denied</code></blockquote>
        </section>

        <hr />

        <section>
          <h3>4. Pergunte sobre etapas, procedimentos ou soluções práticas</h3>
          <blockquote>Quais os comandos para configurar firewall no CentOS 7?</blockquote>
          <blockquote>Como restaurar arquivo de configuração do Apache depois de apagá-lo?</blockquote>
        </section>

        <hr />

        <section>
          <h3>5. Peça explicações simples ou definições</h3>
          <blockquote>O que significa 'inode' no Linux? Pode explicar de forma simples?</blockquote>
          <blockquote>Explique a diferença entre processo e thread no Linux.</blockquote>
        </section>

        <hr />

        <section>
          <h2>Dicas rápidas para prompts eficazes</h2>
          <ul>
            <li>Use frases curtas, claras e diretas.</li>
            <li>Evite termos ambíguos ou perguntas amplas.</li>
            <li>Informe a versão da distribuição Linux.</li>
            <li>Se for erro, detalhe o que já tentou.</li>
          </ul>
        </section>
         <hr />

        <section>
          <h2>Exemplos de prompts bem elaborados</h2>
          <ol className="example-list">
            <li>"No Ubuntu 22.04, ao tentar instalar o MySQL com <code>sudo apt install mysql-server</code>, recebo o erro: 'Erro de dependência: mysql-common'. Como posso resolver isso?"</li>
            <li>"Como criar um script bash que monitore o uso de CPU em tempo real no Linux?"</li>
            <li>"No Debian 11, configurei o SSH para permitir login com chave pública, mas continuo sendo solicitado a senha. O que pode estar errado?"</li>
            <li>"Qual comando uso para verificar quais serviços estão ativos no CentOS 8?"</li>
            <li>"Pode explicar o que é SELinux e como desativá-lo temporariamente para testes?"</li>
            <li>"Estou tentando montar uma unidade de rede NFS no Ubuntu 20.04, mas recebo 'permission denied'. O que devo conferir na configuração?"</li>
            <li>"No Arch Linux, como faço para atualizar apenas um pacote específico sem atualizar todo o sistema?"</li>
            <li>"Quais os passos para configurar um servidor web Apache com suporte a PHP no Fedora 36?"</li>
          </ol>
        </section>

        <hr />

        <section>
          <h2>Casos comuns para guiar seus prompts</h2>
          <ul>
            <li><strong>Instalação e remoção de softwares:</strong> Pergunte sobre comandos e resolução de erros.</li>
            <li><strong>Permissões e acesso:</strong> Problemas com <code>permission denied</code> e configurações de usuários/grupos.</li>
            <li><strong>Configuração de serviços:</strong> SSH, Apache, Nginx, Firewall, etc.</li>
            <li><strong>Scripts e automação:</strong> Bash, crontab, automação de tarefas.</li>
            <li><strong>Monitoramento e diagnóstico:</strong> CPU, memória, logs, status de serviços.</li>
            <li><strong>Rede e conectividade:</strong> IP, DNS, NFS, VPN.</li>
          </ul>
        </section>

        <hr />

        <section>
          <h2>Mais dicas para escrever bons prompts</h2>
          <ul>
            <li>Inclua dados técnicos específicos (versão do SO, kernel, software).</li>
            <li>Copie e cole o erro completo sempre que possível.</li>
            <li>Use aspas para comandos e nomes de arquivos.</li>
            <li>Explique brevemente o que já tentou.</li>
            <li>Peça explicações simples se precisar entender algum termo.</li>
          </ul>
        </section>

        <hr />

        <section>
          <h2>Resumo das melhores práticas</h2>
          <table className="summary-table">
            <thead>
              <tr>
                <th>Dica</th>
                <th>Por quê?</th>
                <th>Exemplo</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Seja específico</td>
                <td>Evita respostas genéricas</td>
                <td>"Como instalar Node.js no Ubuntu"</td>
              </tr>
              <tr>
                <td>Dê contexto</td>
                <td>Ajuda a reproduzir o problema</td>
                <td>"Erro no Ubuntu 22.04"</td>
              </tr>
              <tr>
                <td>Mostre comandos e erros</td>
                <td>Permite diagnóstico preciso</td>
                <td><code>sudo apt update</code> + mensagem</td>
              </tr>
              <tr>
                <td>Pergunte o que deseja</td>
                <td>Direciona a resposta</td>
                <td>"Como faço para..."</td>
              </tr>
              <tr>
                <td>Peça explicações simples</td>
                <td>Facilita entendimento</td>
                <td>"O que é inode?"</td>
              </tr>
            </tbody>
          </table>
        </section>

        <hr />
        <p>Com essas orientações você poderá fazer perguntas mais claras, objetivas e obter respostas úteis e precisas para suas dúvidas e problemas no Linux.</p>
      </main>
    </div>
  );
}
