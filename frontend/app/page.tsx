"use client";

import { useState } from "react";
import axios from "axios";

interface SignalScores {
  wash_trading: number;
  fan_out: number;
  clustering: number;
  velocity: number;
}

interface AnalysisResult {
  wallet: string;
  transactions_analyzed: number;
  overall_score: number;
  risk_level: string;
  signals: SignalScores;
  cached: boolean;
}

export default function Home() {
  const [wallet, setWallet] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState("");

  const analyze = async () => {
    if (!wallet) return;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await axios.post("http://localhost:8000/analyze", {
        wallet,
        limit: 50,
      });
      setResult(res.data);
    } catch (e) {
      setError("Failed to analyze wallet. Check the address and try again.");
    } finally {
      setLoading(false);
    }
  };

  const riskColor = (level: string) => {
    if (level === "high") return "text-red-500";
    if (level === "medium") return "text-yellow-500";
    return "text-green-500";
  };

  const riskBg = (level: string) => {
    if (level === "high") return "bg-red-50 border-red-200";
    if (level === "medium") return "bg-yellow-50 border-yellow-200";
    return "bg-green-50 border-green-200";
  };

  const signalBar = (value: number) => {
    const pct = Math.round(value * 100);
    const color =
      pct >= 70 ? "bg-red-400" : pct >= 40 ? "bg-yellow-400" : "bg-green-400";
    return (
      <div className="flex items-center gap-3">
        <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full ${color}`}
            style={{ width: `${pct}%` }}
          />
        </div>
        <span className="text-sm font-medium w-10 text-right">{pct}%</span>
      </div>
    );
  };

  return (
    <main className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-2xl mx-auto">

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-2xl font-semibold text-gray-900">OpenBCB</h1>
          <p className="text-sm text-gray-500 mt-1">
            Solana wallet anomaly detection — open source AML intelligence
          </p>
        </div>

        {/* Input */}
        <div className="bg-white border border-gray-200 rounded-xl p-5 mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Wallet address
          </label>
          <div className="flex gap-3">
            <input
              type="text"
              value={wallet}
              onChange={(e) => setWallet(e.target.value)}
              placeholder="Enter any Solana wallet address"
              className="flex-1 text-sm border border-gray-200 rounded-lg px-3 py-2 font-mono focus:outline-none focus:ring-2 focus:ring-gray-300"
            />
            <button
              onClick={analyze}
              disabled={loading || !wallet}
              className="px-4 py-2 bg-gray-900 text-white text-sm rounded-lg hover:bg-gray-700 disabled:opacity-40 transition"
            >
              {loading ? "Analyzing..." : "Analyze"}
            </button>
          </div>
          <p className="text-xs text-gray-400 mt-2">
            Try: vines1vzrYbzLMRdu58ou5XTby4qAqVRLmqo36NKPTg
          </p>
        </div>

        {/* Error */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-4 mb-6 text-sm text-red-600">
            {error}
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="space-y-4">

            {/* Overall score */}
            <div className={`border rounded-xl p-5 ${riskBg(result.risk_level)}`}>
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                    Overall risk score
                  </p>
                  <p className={`text-4xl font-semibold mt-1 ${riskColor(result.risk_level)}`}>
                    {result.overall_score}
                    <span className="text-lg font-normal"> / 100</span>
                  </p>
                </div>
                <div className="text-right">
                  <span className={`text-sm font-semibold uppercase ${riskColor(result.risk_level)}`}>
                    {result.risk_level} risk
                  </span>
                  <p className="text-xs text-gray-400 mt-1">
                    {result.transactions_analyzed} txns analyzed
                  </p>
                  {result.cached && (
                    <p className="text-xs text-gray-400">cached result</p>
                  )}
                </div>
              </div>
            </div>

            {/* Signal breakdown */}
            <div className="bg-white border border-gray-200 rounded-xl p-5">
              <p className="text-sm font-medium text-gray-700 mb-4">
                Signal breakdown
              </p>
              <div className="space-y-4">
                {[
                  { key: "wash_trading", label: "Wash trading", desc: "Round-trip transactions" },
                  { key: "fan_out", label: "Fan-out burst", desc: "Sudden multi-wallet sends" },
                  { key: "clustering", label: "Counterparty clustering", desc: "Closed-loop activity" },
                  { key: "velocity", label: "Velocity anomaly", desc: "Transaction frequency" },
                ].map(({ key, label, desc }) => (
                  <div key={key}>
                    <div className="flex justify-between mb-1">
                      <div>
                        <span className="text-sm font-medium text-gray-800">{label}</span>
                        <span className="text-xs text-gray-400 ml-2">{desc}</span>
                      </div>
                    </div>
                    {signalBar(result.signals[key as keyof SignalScores])}
                  </div>
                ))}
              </div>
            </div>

            {/* Wallet */}
            <div className="bg-white border border-gray-200 rounded-xl p-5">
              <p className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">
                Wallet
              </p>
              <p className="text-sm font-mono text-gray-700 break-all">
                {result.wallet}
              </p>
            </div>

          </div>
        )}
      </div>
    </main>
  );
}