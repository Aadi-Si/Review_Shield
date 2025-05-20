import React from "react";
import icon from "/icon.png";
import Button from "./Button";
const TopNav = () => {
  return (
    <nav className="w-screen h-[10vh] bg-[#6872ff] relative flex items-center justify-between px-10">
      <h1 className="white text-3xl font-semibold font-mono text-white flex items-center gap-3">
        <img src={icon} alt="" className="h-[6vh]" />
        Review Shield
      </h1>
      <ul className="flex gap-8">
        <li>
          <Button data={"About"}/>
        </li>
        <li>
          <Button data={"Services"}/>
        </li>
        <li>
          <Button data={"Testimonials"}/> 
        </li>
        <li>
          <Button data={"Contacts"}/>
        </li>
      </ul>
    </nav>
  );
};

export default TopNav;
