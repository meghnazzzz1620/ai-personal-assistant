import React, { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

function Admin({ token }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    const response = await fetch(
      "http://127.0.0.1:8000/admin/analytics",
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );

    const result = await response.json();
    setData(result);
  };

  if (!data) return <div style={{ padding: 40 }}>Loading analytics...</div>;

  return (
    <div style={{ padding: 40, fontFamily: "Arial" }}>
      <h2>Admin Dashboard</h2>

      <div style={{ display: "flex", gap: 20, marginBottom: 30 }}>
        <Card title="Total Users" value={data.total_users} />
        <Card title="Total Messages" value={data.total_messages} />
        <Card title="Total Conversations" value={data.total_conversations} />
      </div>

      <h3>Messages Per User</h3>
      <div style={{ width: "100%", height: 300 }}>
        <ResponsiveContainer>
          <BarChart data={data.messages_per_user}>
            <XAxis dataKey="email" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" fill="#3b82f6" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {data.most_active_user && (
        <>
          <h3 style={{ marginTop: 30 }}>Most Active User</h3>
          <p>
            {data.most_active_user.email} — {data.most_active_user.count} messages
          </p>
        </>
      )}
    </div>
  );
}

function Card({ title, value }) {
  return (
    <div
      style={{
        flex: 1,
        padding: 20,
        backgroundColor: "#f3f4f6",
        borderRadius: 10,
        textAlign: "center"
      }}
    >
      <h4>{title}</h4>
      <h2>{value}</h2>
    </div>
  );
}

export default Admin;
