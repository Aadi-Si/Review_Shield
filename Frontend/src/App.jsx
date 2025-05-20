import React from "react";
import Home from "./components/Home";
import Numbers from "./components/Numbers";
import { Route, Routes } from "react-router-dom";
import Analyze from "./components/Analyze";

const App = () => {
  return (
    <div className="w-full overflow-x-hidden">
      <Routes>
        <Route path="/" element={<Home />}/>
        <Route path="/analyze" element={<Analyze />}/>
      </Routes>
    </div>
  );
};

export default App;
