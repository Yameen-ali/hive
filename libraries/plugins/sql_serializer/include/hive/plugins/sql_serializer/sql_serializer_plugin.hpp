#pragma once
#include <hive/chain/hive_fwd.hpp>
#include <hive/plugins/chain/chain_plugin.hpp>
#include <hive/plugins/sql_serializer/sql_serializer_objects.hpp>

#define HIVE_SQL_SERIALIZER_NAME "sql_serializer"

namespace hive { namespace plugins { namespace sql_serializer {

namespace detail { class sql_serializer_plugin_impl; }

using namespace appbase;
using chain::block_notification;
using chain::transaction_notification;
using chain::operation_notification;
using chain::reindex_notification;

constexpr size_t prereservation_size = 16'000u;

class sql_serializer_plugin final : public plugin<sql_serializer_plugin>
{
  public:
      sql_serializer_plugin();
      virtual ~sql_serializer_plugin();

      APPBASE_PLUGIN_REQUIRES((hive::plugins::chain::chain_plugin))

      static const std::string& name() 
      { 
        static std::string name = HIVE_SQL_SERIALIZER_NAME; 
        return name; 
      }

      void on_pre_reindex(const reindex_notification &note);
      void on_post_reindex(const reindex_notification &note);

      void on_pre_apply_operation(const operation_notification &note);
      void on_pre_apply_block(const block_notification& note);
      void on_post_apply_block(const block_notification &note);
      void on_irreversible_block(uint32_t block_num);

      virtual void set_program_options(options_description& cli, options_description& cfg ) override;
      virtual void plugin_initialize(const variables_map& options) override;
      virtual void plugin_startup() override;
      virtual void plugin_shutdown() override;

      std::mutex& get_currently_persisted_irreversible_mtx();
      std::atomic_uint& get_currently_persisted_irreversible_block();
      std::condition_variable& get_currently_persisted_irreversible_cv();

  private:

      std::unique_ptr<detail::sql_serializer_plugin_impl> my;

      void handle_transactions(const vector<hive::protocol::signed_transaction>& transactions, const uint32_t block_num );
};

} } } //hive::plugins::sql_serializer

