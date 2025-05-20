import React, { useState, useEffect } from 'react';
import CountUp from 'react-countup';
import { useInView } from 'react-intersection-observer';

const Numbers = ({ header, title, para, tail }) => {
  const { ref, inView } = useInView({
    threshold: 0.7,
    triggerOnce: true, // ✅ Ensures it only triggers once
  });

  const [hasAnimated, setHasAnimated] = useState(false);

  useEffect(() => {
    if (inView && !hasAnimated) {
      setHasAnimated(true);
    }
  }, [inView, hasAnimated]);

  return (
    <div
      ref={ref}
      className="h-[32vh] w-[20vw] text-white p-10 rounded-xl border-4"
    >
      <h1 className="font-bold text-5xl">
        {hasAnimated ? (
          <CountUp
            start={0}
            end={header}
            duration={4}
          />
        ) : (
          0
        )}
        {tail}
      </h1>
      <h5 className="mt-5 font-semibold text-xl">{title}</h5>
      <p className="text-[#a0a0a0] w-fit mt-5 font-semibold text-lg">{para}</p>
    </div>
  );
};

export default Numbers;
