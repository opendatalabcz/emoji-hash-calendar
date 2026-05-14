import { useEffect, useState, useContext } from "react";
import { AuthContext } from "../../auth/AuthContext";
import { getUsers, makeAdmin } from "../../api/users";
import "./AdminUserPanel.css";

function AdminUserPanel() {
    const { token } = useContext(AuthContext);
    const [users, setUsers] = useState([]);

    useEffect(() => {
        getUsers(token).then(setUsers).catch(console.error);
    }, [token]);

    const handleMakeAdmin = async (id) => {
        try {
            await makeAdmin(id, token);
            const updated = await getUsers(token);
            setUsers(updated);
        } catch (err) {
            alert(err.message);
        }
    };

    return (
        <div className="admin-user-panel">
            <h3>User Management</h3>
            <p className="admin-description">
                Give users admin role to allow them to manage dictionaries.
            </p>

            <div className="admin-card">
                <table className="user-table">
                    <thead>
                    <tr>
                        <th>ID</th>
                        <th>Username</th>
                        <th>Admin</th>
                        <th>Actions</th>
                    </tr>
                    </thead>

                    <tbody>
                    {users.map((u) => (
                        <tr key={u.id}>
                            <td>{u.id}</td>
                            <td>{u.username}</td>
                            <td>
                                {u.is_admin ? (
                                    <span className="admin-badge">Admin</span>
                                ) : (
                                    <span className="user-badge">User</span>
                                )}
                            </td>
                            <td>
                                {!u.is_admin && (
                                    <button
                                        className="make-admin-btn"
                                        onClick={() => handleMakeAdmin(u.id)}
                                    >
                                        Make Admin
                                    </button>
                                )}
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default AdminUserPanel;
