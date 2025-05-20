import React, { useEffect, useState } from "react";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import TopNav from "../../src/components/TopNav";
const COLORS = ["#34d399", "#f87171"]; // green for real, red for fake

const Analyze = () => {
  const [loading, setLoading] = useState(true);
  const [reviews, setReviews] = useState([]);
  const [productName, setProductName] = useState("");
  const [images, setImages] = useState([]);
  const [error, setError] = useState("");
  const [recommendation, setRecommendation] = useState("");
  const [stats, setStats] = useState(null);

  useEffect(() => {
    const fetchReviews = async () => {
      const url = localStorage.getItem("productURL");

      try {
        const res = await fetch("http://localhost:5000/api/review", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ url }),
        });

        const data = await res.json();

        if (res.ok) {
          setProductName(data.product_name);
          setReviews(data.reviews);
          setImages(data.images);
          setRecommendation(data.overall_rating);
          setStats(data.stats);
        } else {
          setError(data.error || "Something went wrong.");
        }
      } catch (err) {
        setError("Failed to fetch data from server.");
      } finally {
        setLoading(false);
      }
    };

    fetchReviews();
  }, []);

  const chartData = stats
    ? [
        { name: "Real Reviews", value: stats.real },
        { name: "Fake Reviews", value: stats.fake },
      ]
    : [];

  if (loading) return <div className="text-white">Loading...</div>;
  if (error) return <div className="text-red-500">{error}</div>;

  return (
    <div className="text-white">
      <TopNav />
      <div className="p-10">
        <div className=" w-full p-10 flex rounded-2xl border-4  border-white">
          <div className="mr-10 mt-10">
            <div className="w-[12vw] h-[30vh] mb-6 bg-white rounded-xl overflow-hidden ml-4">
              {images.map((src, i) => (
                <img
                  key={i}
                  src={src}
                  alt="Product"
                  className="object-contain h-[30vh] w-full"
                />
              ))}
            </div>
            {recommendation && (
              <div
                className={`mb-6 rounded text-lg font-semibold h-[7vh] w-fit text-white`}
              >
                {recommendation}
              </div>
            )}
          </div>

          {stats && (
            <>
              <div className="bg-zinc-900 p-4 rounded mb-6 border-2 border-zinc-500 w-[55vw]">
                <h1 className="text-2xl font-black mb-7 w-full h-15">
                  {productName.split(" ").length > 0
                    ? productName.split(" ").slice(0, 12).join(" ") + " more..."
                    : productName}
                </h1>
                <div className="flex p-4">
                  <div className=" pt-10 h-[36vh]">
                    <h2 className="text-xl font-bold mb-4">
                      Review Analysis Summary
                    </h2>
                    <p className="text-lg font-semibold mb-3">
                      Total Reviews Processed :{" "}
                      <span className="text-blue-400 text-xl">
                        {stats.total}
                      </span>
                    </p>
                    <p className="text-lg font-semibold mb-4">
                      Real Reviews :{" "}
                      <span className="text-green-400 text-xl">
                        {stats.real}
                      </span>{" "}
                      ({stats.real_percent.toFixed(1)}%)
                    </p>
                    <p className="text-lg font-semibold mb-4">
                      Fake Reviews :{" "}
                      <span className="text-red-400 text-xl">{stats.fake}</span>{" "}
                      ({stats.fake_percent.toFixed(1)}%)
                    </p>
                  </div>
                  {/*✅ Pie Chart */}
                  <div className="bg-zinc-900 rounded mb-6 w-[20vw] ml-20">
                    <div className="mt-0">
                      <ResponsiveContainer width="100%" height={230}>
                        <PieChart>
                          <Pie
                            data={chartData}
                            cx="50%"
                            cy="50%"
                            labelLine={false}
                            outerRadius={80}
                            fill="#8884d8"
                            dataKey="value"
                          >
                            {chartData.map((entry, index) => (
                              <Cell
                                key={`cell-${index}`}
                                fill={COLORS[index % COLORS.length]}
                              />
                            ))}
                          </Pie>
                          <Tooltip />
                          <Legend />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>
              </div>

              {/* ✅ Grade Display */}
              <div className="bg-zinc-900 p-4 rounded mb-6 w-[20vw] ml-10 border-2 border-zinc-500">
                <h2 className="text-2xl font-black mb-2 px-5">
                  Review Shield Grade
                </h2>
                <p className="h-[10vh] w-[20vh] bg-green-400 p-4 rounded-2xl mt-10 ml-15">
                  <span className="text-white text-5xl font-semibold ml-11">
                    {stats.grade}
                  </span>
                </p>
                <div className="text-lg font-semibold text-zinc-300 mt-10 pl-18">
                  <h5 className="mb-2">If Score {">"} 90 : A+</h5>
                  <h5 className="mb-2">If Score {">"} 80 : A</h5>
                  <h5 className="mb-2">If Score {">"} 70 : B</h5>
                  <h5 className="mb-2">If Score {">"} 60 : C</h5>
                  <h5 className="mb-2">If Score {"<"} 50 : D</h5>
                </div>
              </div>
            </>
          )}
        </div>

        {reviews.map((r, index) => (
          <div key={index} className="bg-zinc-800 p-5 px-10 rounded mb-4 mt-10">
            <h2 className="text-2xl font-semibold">{r.CommentHead}</h2>
            <p className="text-yellow-400 mt-3 text-xl">
              Rating : ⭐{r.Rating}
            </p>
            <p className="text-zinc-400 italic mt-3 text-lg">by {r.Name}</p>
            <p className="mt-3 text-xl">{r.Comment}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Analyze;
