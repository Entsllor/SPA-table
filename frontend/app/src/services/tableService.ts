import {AxiosResponse} from "axios";
import {TableRow, IOrderingFields} from "../interfaces";
import {api} from "./api";

export default class TableService {
    static async getRows(ordering: IOrderingFields = {}): Promise<AxiosResponse<TableRow[]>> {
        let orderingParams = '';
        if (ordering) {
            for (let [key, value] of Object.entries(ordering)) {
                let queryParamValue = value? key : `-${key}`
                orderingParams += `ordering_fields=${queryParamValue}&`
            }
        }

        return api.get(
            `table/rows/?${orderingParams}`,
            {
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem("JWT")}`
                }
            }
        );
    }
}
