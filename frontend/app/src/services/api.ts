import axios from "axios";


export const API_URL = "http://localhost:8000/"

export const api = axios.create({
    withCredentials: true,
    baseURL: API_URL
})

api.interceptors.response.use((config) => {
    return config;
}, (async (error) => {
    if (error.response.status == 401) {
        let response = await axios.post(`${API_URL}revoke/`, null, {withCredentials: true});
        if (response.status != 401) {

            localStorage.setItem("JWT", response.data.access_token);
            return response;
        } else {
            localStorage.setItem("JWT", "")
        }
    }
}))
