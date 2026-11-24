import React from "react";

import { Routes, Route } from "react-router";

import Sidebar from "./components/Sidebar";
import Dashboard from "./page/Dashboard";
import Home from "./page/Home";
import SignUp from "./components/SignUp";

const App: React.FC = () => {
  return (
      <div className="container-fluid">
        <div className="row flex-nowrap">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/signup" element={<SignUp />} />
          </Routes>
        </div>
      </div>
  );
};

export default App;