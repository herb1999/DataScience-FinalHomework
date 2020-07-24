import { axios } from '@/utils/request'
export function testAPI(){
    return axios({
        url: '/test',
        method: 'GET'
    })
}
export function allCasesAPI() {
    return axios({
        url: '/allCases',
        method: 'GET',
    })
}
export function caseMdAPI(caseId) {
    return axios({
        url: '/caseMd',
        method: 'GET',
        params:{caseId}
    })
}
export function recommendLabelAPI(caseId) {
    return axios({
        url: '/recommendLabel',
        method: 'GET',
        params:{caseId}
    })
}
export function commitCodeAPI(data) {
    return axios({
        url: '/commitCode',
        method: 'POST',
        data
    })
}
export function recommendCodeAPI(caseId) {
    return axios({
        url: '/recommendCode',
        method: 'GET',
        params:{caseId}
    })
}
