import React, { useState } from "react";
import { Link } from "react-router-dom";
import TopNav from "./TopNav";
import Button from "./Button";
import main_image from "/main0.jpeg";
import Numbers from "./Numbers";

const Home = () => {
  const [url, setUrl] = useState("");

  const handleAnalyzeClick = () => {
    localStorage.setItem("productURL", url);
  };
  return (
    <div className="w-screen h-screen">
      <TopNav />
      <div className="h-[80vh] w-full flex mt-10">
        <div className="h-full w-[45%]  pt-15 text-white px-20">
          <h1 className="text-8xl font-black  text-white">
            Detect Fake
            <br />
            Reviews
            <br />
            Effortlessly
          </h1>
          <p className="text-zinc-500 text-xl pt-10">
            Our platform specializes in identifying and verifying the
            authenticity of product reviews on e-commerce websites, empowering
            you to make informed purchasing decisions.
          </p>
          <div className="flex gap-10 mt-10">
            <Button data={"Get Started"} />
            <button className="px-3 py-3 cursor-pointer font-semibold text-md border-3 rounded-md">
              Learn More
            </button>
          </div>
        </div>
        <div className="h-full w-[55%] p-2 pt-15">
          <img src={main_image} alt="" className="w-fit h-fit object-cover" />
        </div>
      </div>
      <div className="mt-20 h-[40vh] w-full flex flex-wrap p-10 gap-12 pl-22">
        <Numbers
          header={50}
          tail={"K+"}
          title={"Products analyzed"}
          para={"Number of products reviewed for authenticity"}
        />
        <Numbers
          header={95}
          tail={"%"}
          title={"Accuracy rate"}
          para={"Percentage of accurate fake review detection"}
        />
        <Numbers
          header={75}
          tail={"K+"}
          title={"Satisfied users"}
          para={"Users who trust our detection system"}
        />
        <Numbers
          header={24}
          tail={"/7"}
          title={"Support available"}
          para={"Round-the-clock assistance for users"}
        />
      </div>
      <div className="h-[40vh] w-full flex p-10 items-center justify-center">
        <input
          type="text"
          className="bg-white w-[25vw] h-[6vh] mr-10 rounded-xl font-semibold text-zinc-500 px-5 outline-none text-lg"
          placeholder="Paste link to analyze a product"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <Link
          to="/analyze"
          onClick={handleAnalyzeClick}
          className="bg-[#6275ff] h-[6vh] w-fit text-white font-semibold px-3 py-3 rounded-md text-md"
        >
          Analyze
        </Link>
      </div>
    </div>
  );
};

export default Home;
