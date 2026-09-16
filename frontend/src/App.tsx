import { useEffect, useState } from "react";
import "./styles/calculator.css";

type Operator = "+" | "-" | "×" | "÷";
const operators: Operator[] = ["+", "-", "×", "÷"];

const calculatorApiUrl = import.meta.env.VITE_CALCULATOR_API_URL ?? "http://localhost:8000/api/v1/calculate/";

function App() {
  const [expression, setExpression] = useState("0");
  const [previous, setPrevious] = useState("");
  const [justCalculated, setJustCalculated] = useState(false);
  const [isCalculating, setIsCalculating] = useState(false);
  const calculate = async () => {
    setIsCalculating(true);
    try {
      const response = await fetch(calculatorApiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ expression }),
      });
      const data: { result?: string; detail?: string } = await response.json();
      if (!response.ok || !data.result) throw new Error(data.detail ?? "Calculation failed.");
      setPrevious(`${expression} =`);
      setExpression(data.result);
    } catch {
      setPrevious(expression);
      setExpression("Error");
    } finally {
      setJustCalculated(true);
      setIsCalculating(false);
    }
  };
  const input = (key: string) => {
    if (key === "C") { setExpression("0"); setPrevious(""); setJustCalculated(false); return; }
    if (key === "⌫") { setExpression((value) => value.length <= 1 || value === "Error" ? "0" : value.slice(0, -1)); setJustCalculated(false); return; }
    if (key === "=") { void calculate(); return; }
    if (key === "+/−") { setExpression((value) => value === "0" ? "0" : value.startsWith("-") ? value.slice(1) : `-${value}`); return; }
    const isOperator = operators.includes(key as Operator);
    setExpression((value) => {
      const current = value === "Error" ? "0" : value;
      if (isOperator) return operators.includes(current.slice(-1) as Operator) ? `${current.slice(0, -1)}${key}` : `${current}${key}`;
      if (key === ".") { const last = current.split(/[+\-×÷]/).pop() ?? ""; return last.includes(".") ? current : `${current}.`; }
      return justCalculated ? key : current === "0" ? key : `${current}${key}`;
    });
    setJustCalculated(false);
  };
  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      const mapped: Record<string, string> = { "*": "×", "/": "÷", Enter: "=", "=": "=", Escape: "C", Backspace: "⌫" };
      const key = mapped[event.key] ?? event.key;
      if (!isCalculating && (/^\d$/.test(key) || [".", "+", "-", "×", "÷", "=", "C", "⌫"].includes(key))) { event.preventDefault(); input(key); }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [isCalculating]);
  const buttons = ["C", "+/−", "÷", "⌫", "7", "8", "9", "×", "4", "5", "6", "-", "1", "2", "3", "+", "0", ".", "="];
  return <main className="app-shell" aria-label="Calculator application"><section className="calculator" aria-label="Calculator"><header className="calculator__header"><span className="calculator__mark">◌</span><span>CALCULATOR</span></header><output className="calculator__display" aria-live="polite"><span className="calculator__previous">{previous || " "}</span><span className="calculator__expression">{isCalculating ? "Calculating…" : expression}</span></output><div className="calculator__keys">{buttons.map((button) => <button key={button} className={`key key--${button === "=" ? "equals" : operators.includes(button as Operator) ? "operator" : ["C", "+/−", "⌫"].includes(button) ? "utility" : "number"}`} onClick={() => input(button)} disabled={isCalculating} type="button">{button}</button>)}</div></section></main>;
}

export default App;
