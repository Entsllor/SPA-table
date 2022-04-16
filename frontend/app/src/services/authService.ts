import {AxiosResponse} from "axios";
import {api} from "./api";

export default class AuthService {
    static async login(username: string, password: string): Promise<AxiosResponse<{ access_token: string }>> {
        return api.post(
            "login/",
            `username=${username}&password=${password}`,
            {headers: {"Content-Type": "application/x-www-form-urlencoded"}}
        ).then(response => {
            localStorage.setItem("JWT", response.data.access_token);
            return response
        })
    }

    static async registration(username: string, password: string, email: string): Promise<AxiosResponse<{}>> {
        return api.post(
            "users/",
            {username: username, password: password, email: email},
        )
    }

    static async revoke(): Promise<AxiosResponse<{ access_token: string }>> {
        return api.post("revoke/").then(response => {
            localStorage.setItem("JWT", response.data.access_token);
            return response
        })
    }

    static async aboutMe(): Promise<AxiosResponse> {
        return api.get(
            "users/me/",
            {
                headers: {
                    "Authorize": `Bearer ${localStorage.getItem("JWT")}`
                }
            }
        )
    }
}