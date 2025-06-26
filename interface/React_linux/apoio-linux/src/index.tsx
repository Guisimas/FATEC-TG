import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import App from "@pages/app";
import PromptDesign from "@pages/promptDesign";

const root = ReactDOM.createRoot(document.getElementById("root") as HTMLElement);
root.render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/prompt-design" element={<PromptDesign />} />
    </Routes>
  </BrowserRouter>
);
