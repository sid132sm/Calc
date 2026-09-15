import { useEffect, useState } from "react";
import "./styles/calculator.css";

type Operator = "+" | "-" | "×" | "÷";
const operators: Operator[] = ["+", "-", "×", "÷"];

function calculate(expression: string) {
  const tokens = expression.match(/\d*\.?\d+|[+\-×÷]/g);
  if (!tokens?.length || tokens.join("") !== expression) throw new Error("Invalid expression");
  const values: number[] = [];
  const pending: Operator[] = [];
  const priority = (operator: Operator) => (operator === "×" || operator === "÷" ? 2 : 1);
  const apply = () => {
    const operator = pending.pop(); const right = values.pop(); const left = values.pop();
    if (!operator || left === undefined || right === undefined) throw new Error("Invalid expression");
    values.push(operator === "+" ? left + right : operator === "-" ? left - right : operator === "×" ? left * right : left / right);
  };
  for (const token of tokens) {
    if (operators.includes(token as Operator)) {
      const operator = token as Operator;
      while (pending.length && priority(pending[pending.length - 1]) >= priority(operator)) apply();
      pending.push(operator);
    } else values.push(Number(token));
  }
  while (pending.length) apply();
  if (values.length !== 1 || !Number.isFinite(values[0])) throw new Error("Invalid expression");
  return Number.parseFloat(values[0].toPrecision(12)).toString();
}

function App() {
  const [expression, setExpression] = useState("0");
  const [previous, setPrevious] = useState("");
  const [justCalculated, setJustCalculated] = useState(false);
  const input = (key: string) => {
    if (key === "C") { setExpression("0"); setPrevious(""); setJustCalculated(false); return; }
    if (key === "⌫") { setExpression((value) => value.length <= 1 || value === "Error" ? "0" : value.slice(0, -1)); setJustCalculated(false); return; }
    if (key === "=") { try { const result = calculate(expression); setPrevious(`${expression} =`); setExpression(result); } catch { setPrevious(expression); setExpression("Error"); } setJustCalculated(true); return; }
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
      if (/^\d$/.test(key) || [".", "+", "-", "×", "÷", "=", "C", "⌫"].includes(key)) { event.preventDefault(); input(key); }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  });
  const buttons = ["C", "+/−", "÷", "⌫", "7", "8", "9", "×", "4", "5", "6", "-", "1", "2", "3", "+", "0", ".", "="];
  return <main className="app-shell" aria-label="Calculator application"><section className="calculator" aria-label="Calculator"><header className="calculator__header"><span className="calculator__mark">◌</span><span>CALCULATOR</span></header><output className="calculator__display" aria-live="polite"><span className="calculator__previous">{previous || " "}</span><span className="calculator__expression">{expression}</span></output><div className="calculator__keys">{buttons.map((button) => <button key={button} className={`key key--${button === "=" ? "equals" : operators.includes(button as Operator) ? "operator" : ["C", "+/−", "⌫"].includes(button) ? "utility" : "number"}`} onClick={() => input(button)} type="button">{button}</button>)}</div></section></main>;
}

export default App;
