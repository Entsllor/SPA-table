import {AxiosResponse} from "axios";
import {TableRow, IOrderingFields} from "../interfaces";
import {api} from "./api";

export default class TableService {
    static async getRows(
        ordering: IOrderingFields = {},
        page?: number,
        pageSize = 10,
        filter?: string
    ): Promise<AxiosResponse<TableRow[]>> {
        let queryParams = '';
        if (ordering) {
            for (let [key, value] of Object.entries(ordering)) {
                let queryParamValue = value ? key : `-${key}`
                queryParams += `ordering_fields=${queryParamValue}&`
            }
        }
        if (page) {
            queryParams += `offset=${(page - 1) * pageSize}&`
            queryParams += `limit=${pageSize}&`
        }
        if (filter) {
            queryParams += `filter_by=${filter}&`
        }

        return api.get(
            `table/rows/?${queryParams}`,
            {
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem("JWT")}`
                }
            }
        );
    }
}
