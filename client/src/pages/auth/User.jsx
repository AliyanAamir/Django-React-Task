import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import useAuth from "../../hooks/useAuth";
import useLogout from "../../hooks/useLogout";
import useUser from "../../hooks/useUser";

export default function User() {
  const { user } = useAuth();

  const navigate = useNavigate();
  const logout = useLogout();
  const [loading, setLoading] = useState(false);
  const getUser = useUser();

  useEffect(() => {
    getUser();
  }, []);

  async function onLogout() {
    setLoading(true);

    await logout();
    navigate("/");
  }

  return (
    <div className="container mt-3">
      <h4>User Id : {user?.id}</h4>
      <h4>UserName : {user?.username}</h4>
      <h4>Email : {user?.email}</h4>
      <h4>First Name : {user?.first_name}</h4>
      <h4>Last Name : {user?.last_name}</h4>
      <h4>{user?.is_staff}</h4>
      <h4>Ethereum Wallet Address: {user?.ethereum_address}</h4>
      <h4>
        Ethereum Wallet Balance: {parseFloat(user?.ethereum_balance).toFixed(4)}
      </h4>
      <button disabled={loading} type="button" onClick={onLogout}>
        Logout
      </button>
    </div>
  );
}
