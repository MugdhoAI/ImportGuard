import React from "react";
import { createRoot } from "react-dom/client";
import { Landing } from "./pages/Landing";
import "./styles/tokens.css";
import "./styles/landing.css";

createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <Landing />
  </React.StrictMode>,
);
