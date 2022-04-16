import {AxiosResponse} from "axios";
import TableRow from "../interfaces";
import {api} from "./api";

export default class TableService {
    static async getRows(): Promise<AxiosResponse<TableRow[]>> {
        return api.get(
            "table/rows/",
            {
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem("JWT")}`
                }
            }
        );
    }
}
