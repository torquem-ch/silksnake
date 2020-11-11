#include <optional>
#include <sstream>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <silkworm/common/util.hpp>
#include <silkworm/types/transaction.hpp>

#include "transaction.hpp"
#include "types.hpp"
#include "uint256_type_caster.hpp"

namespace py = pybind11;

using namespace silkworm;

std::ostream& operator<<(std::ostream& out, const Transaction& t) {
    out << "nonce=" << std::to_string(t.nonce)
        << " gas_price=" << t.gas_price
        << " gas_limit=" << std::to_string(t.gas_limit)
        << " to=" << (t.to.has_value() ? t.to.value() : evmc::address{})
        << " value=" << t.value
        << " data=0x" << to_hex(t.data).substr(0, 8) << (t.data.length() > 0 ? "..." : "")
        << " from=" << (t.from.has_value() ? t.from.value() : evmc::address{});
    return out;
}

void bind_transaction(py::module_& module) {
    py::class_<Transaction>(module, "Transaction")
        .def(py::init([](
            uint64_t nonce,
            intx::uint256 gas_price,
            uint64_t gas_limit,
            std::optional<evmc::address> to,
            intx::uint256 value,
            const std::string& data_bytes, // use Pybind11 builtin type conversion from bytes to std::string
            intx::uint256 v,
            intx::uint256 r,
            intx::uint256 s,
            std::optional<evmc::address> from) {
                Bytes data(data_bytes.begin(), data_bytes.end()); // use C++ builtin conversion from char to uint8_t
                return Transaction{nonce, gas_price, gas_limit, to, value, data, v, r, s, from};
        }))
        .def_readwrite("nonce", &Transaction::nonce)
        .def_readwrite("gas_price", &Transaction::gas_price)
        .def_readwrite("gas_limit", &Transaction::gas_limit)
        .def_readwrite("to", &Transaction::to)
        .def_readwrite("value", &Transaction::value)
        .def_readwrite("data", &Transaction::data)
        .def_readwrite("v", &Transaction::v)
        .def_readwrite("r", &Transaction::r)
        .def_readwrite("s", &Transaction::s)
        .def_readwrite("from", &Transaction::from)
        .def("__repr__", [](const Transaction& t) {
            std::ostringstream oss;
            oss << "<silkworm::Transaction " << t << ">";
            return oss.str();
        });
}
